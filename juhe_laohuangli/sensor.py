"""
The chinese 老黄历 information comes from Juhe.

by HAChina.io

"""
import asyncio
import async_timeout
import aiohttp
import logging
import json
from datetime import timedelta
import voluptuous as vol

from homeassistant.helpers.aiohttp_client import async_get_clientsession
import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import ATTR_ATTRIBUTION
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.event import async_track_time_change
import homeassistant.util.dt as dt_util

_LOGGER = logging.getLogger(__name__)


CONF_ATTRIBUTION = "Today's laohuangli provided by Juhe"
CONF_KEY = 'key'

DEFAULT_NAME = 'LaoHuangLi'
ICON = 'mdi:yin-yang'


PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_KEY):cv.string,
})

@asyncio.coroutine
def async_setup_platform(hass, config, async_add_devices, discovery_info=None):
    """Set up the laohuangli sensor."""

    key = config.get(CONF_KEY)

    data = JuheLaohuangliData(hass, key)
    yield from data.async_update(dt_util.now())
    async_track_time_change( hass, data.async_update, hour=[0], minute=[0], second=[1] )

    dev = []
    dev.append(JuheLaohuangliSensor(data))
    async_add_devices(dev, True)


class JuheLaohuangliSensor(Entity):
    """Representation of a Juhe Laohuangli sensor."""

    def __init__(self, data):
        """Initialize the sensor."""
        self._data = data
        self._name = DEFAULT_NAME

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name


    @property
    def state(self):
        """Return the state of the sensor."""
        return self._data.yinli

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        if self._data is not None:
            return {
                "阳历": self._data.yangli,
                "阴历": self._data.yinli,
                "五行": self._data.wuxing,
                "冲煞": self._data.chongsha,
                "百忌": self._data.baiji,
                "吉神": self._data.jishen,
                "宜": self._data.yi,
                "凶神": self._data.xiongshen,
                "忌": self._data.ji,
            }

    @property
    def icon(self):
        """Return the icon to use in the frontend, if any."""
        return ICON
    
    @asyncio.coroutine
    def async_update(self):
        """Get the latest data and updates the states."""



class JuheLaohuangliData(object):
    """Get data from Juhe laohuangli imformation."""

    def __init__(self, hass, key):
        """Initialize the data object."""


        self.yangli = None
        self.yinli = None
        self.wuxing = None
        self.chongsha = None
        self.baiji = None
        self.jishen = None
        self.yi = None
        self.xiongshen = None
        self.ji = None
        
        self.hass = hass

        self.url = "http://v.juhe.cn/laohuangli/d"
        self.key = key


    @asyncio.coroutine
    def async_update(self, now):
        """Get the latest data and updates the states."""

        date = now.strftime("%Y-%m-%d")
        params = {
            "key": self.key,
            "date": date,
            }

        try:
            session = async_get_clientsession(self.hass)
            with async_timeout.timeout(15, loop=self.hass.loop):
                response = yield from session.post( self.url, data=params )

        except(asyncio.TimeoutError, aiohttp.ClientError):
            _LOGGER.error("Error while accessing: %s", self.url)
            return

        if response.status != 200:
            _LOGGER.error("Error while accessing: %s, status=%d", url, response.status)
            return

        result = yield from response.json()

        if result is None:
            _LOGGER.error("Request api Error: %s", url)
            return
        elif (result["error_code"] != 0):
            _LOGGER.error("Error API return, errorcode=%s, reson=%s",
                          result["error_code"],
                          result["reason"],
                          )
            return
        
        
        self.yangli = result["result"]["yangli"]
        self.yinli = result["result"]["yinli"]
        self.wuxing = result["result"]["wuxing"].replace(" ","、")
        self.chongsha = result["result"]["chongsha"]
        self.baiji = result["result"]["baiji"].replace(" ","、")
        self.jishen = result["result"]["jishen"].replace(" ","、")
        self.yi = result["result"]["yi"].replace(" ","、")
        self.xiongshen = result["result"]["xiongshen"].replace(" ","、")
        self.ji = result["result"]["ji"].replace(" ","、")
