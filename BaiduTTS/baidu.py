"""
Baidu TTS　HAChina
"""
import asyncio
import logging
import re

import aiohttp
import async_timeout
import voluptuous as vol


from homeassistant.components.tts import Provider, PLATFORM_SCHEMA, CONF_LANG
import homeassistant.helpers.config_validation as cv


REQUIREMENTS = ["baidu-aip==1.6.6"]

_LOGGER = logging.getLogger(__name__)


SUPPORT_LANGUAGES = [
    'zh',
]
DEFAULT_LANG = 'zh'


CONF_APPID = 'appid'
CONF_APIKEY = 'apikey'
CONF_SECRETKEY = 'secretkey'
CONF_SPEED = 'speed'
CONF_PITCH = 'pitch'
CONF_VOLUME = 'volume'
CONF_PERSON = 'person'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_LANG, default=DEFAULT_LANG): vol.In(SUPPORT_LANGUAGES),
    vol.Required(CONF_APPID): cv.string,
    vol.Required(CONF_APIKEY): cv.string,
    vol.Required(CONF_SECRETKEY): cv.string,
    vol.Optional(CONF_SPEED, default=5): vol.All(vol.Coerce(int), vol.Range(min=0,max=9)),
    vol.Optional(CONF_PITCH, default=5): vol.All(vol.Coerce(int), vol.Range(min=0,max=9)),
    vol.Optional(CONF_VOLUME, default=5): vol.All(vol.Coerce(int), vol.Range(min=0,max=15)),
    vol.Optional(CONF_PERSON, default=0): vol.All(vol.Coerce(int), vol.Range(min=0,max=4)),
    
})


@asyncio.coroutine
def async_get_engine(hass, config):
    """Set up Baidu TTS component."""
    return BaiduTTSProvider(hass, config)


class BaiduTTSProvider(Provider):
    """Baidu TTS speech api provider."""

    def __init__(self, hass, conf):
        """Init Baidu TTS service."""
        self.hass = hass
        self._lang = conf.get(CONF_LANG)
        self._appid = conf.get(CONF_APPID)
        self._apikey = conf.get(CONF_APIKEY)
        self._secretkey = conf.get(CONF_SECRETKEY)

        self._speed = conf.get(CONF_SPEED)
        self._pitch = conf.get(CONF_PITCH)
        self._volume = conf.get(CONF_VOLUME)
        self._person = conf.get(CONF_PERSON)
        
        self._codec = 'mp3'
        self.name = 'BaiduTTS'

    @property
    def default_language(self):
        """Return the default language."""
        return self._lang

    @property
    def supported_languages(self):
        """Return list of supported languages."""
        return SUPPORT_LANGUAGES

    @asyncio.coroutine
    def async_get_tts_audio(self, message, language, options=None):
        """Load TTS from BaiduTTS."""
        from aip import AipSpeech
        aipSpeech = AipSpeech( self._appid, self._apikey, self._secretkey )

        result = aipSpeech.synthesis( message, language, 1,
                                      {'spd':self._speed,
                                       'pit':self._pitch,
                                       'vol':self._volume,
                                       'per':self._person
                                       },                                      
                                      )

        if isinstance(result, dict):
            _LOGGER.error('Baidu TTS error-- err_no:',
                          result['err_no'],
                          '; err_msg:',
                          result['err_msg'],
                          '; err_detail:',
                          result['err_detail']
                         )
            return (None, None)

        return (self._codec, result)

