"""
Support for PulseAudio speakers(sinks)

"""
import voluptuous as vol
import asyncio
import logging
import urllib.request
import numpy as np

import soundcard as sc

from homeassistant.components.media_player.const import (
    SUPPORT_PLAY_MEDIA, MEDIA_TYPE_MUSIC)
from homeassistant.components.media_player import (
    MediaPlayerEntity, PLATFORM_SCHEMA)
from homeassistant.const import (
    CONF_NAME, STATE_IDLE, STATE_PLAYING)
import homeassistant.helpers.config_validation as cv
from homeassistant.components.ffmpeg import DATA_FFMPEG

from .mm2pcm import PCMStream

from .const import (
    DOMAIN,
    CONF_SINK,
    DEFAULT_NAME,
    DEFAULT_SINK,
)

SUPPORT_PULSEAUDIO = SUPPORT_PLAY_MEDIA

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Optional(CONF_SINK, default=DEFAULT_SINK): cv.string,
})

_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Setup the Pulse Audio Speaker platform."""
    name = config.get(CONF_NAME)
    sink = config.get(CONF_SINK)

    async_add_entities([PulseAudioSpeaker(hass, name, sink)])
    return True


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Add Pulse Audio entities from a config_entry."""
    name = config_entry.data[CONF_NAME]
    sink = config_entry.data[CONF_SINK]

    async_add_entities([PulseAudioSpeaker(hass, name, sink)])


class PulseAudioSpeaker(MediaPlayerEntity):
    """Representation of a Pulse Audio Speaker local."""

    def __init__(self, hass, name, sink):
        """Initialize the device."""

        self._hass = hass
        self._name = name
        self._state = STATE_IDLE
        self._manager = hass.data[DATA_FFMPEG]
        self.sink = sink

    @property
    def name(self):
        """Return the name of the device."""
        return self._name

    @property
    def state(self):
        """Return the state of the device."""
        return self._state

    @property
    def supported_features(self):
        """Flag media player features that are supported."""
        return SUPPORT_PULSEAUDIO

    def play_media(self, media_type, media_id, **kwargs):
        """Send play commmand."""
        if not media_type == MEDIA_TYPE_MUSIC:
            _LOGGER.error(
                "Invalid media type %s. Only %s is supported",
                media_type,
                MEDIA_TYPE_MUSIC,
            )
            return

        if(sink == DEFAULT_SINK):
            speaker = sc.default_speaker()
        else:
            speaker = sc.get_speaker(sink)

        _LOGGER.info('play_media: %s', media_id)
        self._state = STATE_PLAYING
        self.schedule_update_ha_state()

        try:
            local_path, _ = urllib.request.urlretrieve(media_id)
        # urllib.error.HTTPError
        except Exception:  # pylint: disable=broad-except
            local_path = media_id

        stream = PCMStream(self._manager.binary, loop=self._hass.loop)
        stream_reader = asyncio.run_coroutine_threadsafe(
            stream.PCMStreamReader(input_source=local_path),
            self._hass.loop).result()

        data = asyncio.run_coroutine_threadsafe(
                        stream_reader.read(-1), self._hass.loop).result()
        data = np.frombuffer(data, dtype=np.int16)/pow(2,15)

        speaker.play(data, samplerate=16000, channels=1)

        urllib.request.urlcleanup()
        self._state = STATE_IDLE
        self.schedule_update_ha_state()