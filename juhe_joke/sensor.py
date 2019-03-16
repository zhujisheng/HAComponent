"""
The chinese jokes come from Juhe.

by HAChina.io

"""
import logging
import json
from urllib import request, parse
from random import randint
import asyncio
from datetime import timedelta

import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import (DOMAIN,PLATFORM_SCHEMA)
from homeassistant.const import (ATTR_ATTRIBUTION, CONF_NAME)
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.event import async_track_time_change
import homeassistant.util.dt as dt_util

_LOGGER = logging.getLogger(__name__)


CONF_ATTRIBUTION = "Today's jokes provided by Juhe"
CONF_KEY = 'key'

DEFAULT_NAME = 'Jokes'
ICON = 'mdi:book-open-variant'


PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_KEY):cv.string,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
})

@asyncio.coroutine
def async_setup_platform(hass, config, async_add_devices, discovery_info=None):
    """Set up the joke sensor."""

    key = config.get(CONF_KEY)
    name = config.get(CONF_NAME)

    dev = []
    data = JuheJokeData(hass, key)
    sensor = JuheJokeSensor(data, name)
    dev.append(sensor)

    async_add_devices(dev, True)

    def update(call=None):
        '''Update the data by service call'''
        data.update(dt_util.now())
        sensor.async_update()

    hass.services.async_register(DOMAIN, name+'_update',update)

        


class JuheJokeSensor(Entity):
    """Representation of a Juhe Joke sensor."""

    def __init__(self, data, name):
        """Initialize the sensor."""
        self._data = data
        self._name = name

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name


    @property
    def state(self):
        """Return the state of the sensor."""
        return self._data.state

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        if self._data.state is not None:
            return self._data.story

    @property
    def icon(self):
        """Return the icon to use in the frontend, if any."""
        return ICON
    
    @asyncio.coroutine
    def async_update(self):
        """Get the latest data and updates the states."""



class JuheJokeData(object):
    """Get data from Juhe Joke imformation."""

    def __init__(self, hass, key):
        """Initialize the data object."""


        self.story = {}
        self.hass = hass

        self.url = "http://v.juhe.cn/joke/content/text.php"
        self.key = key

        self.state = None

        self.update(dt_util.now())
        async_track_time_change( self.hass, self.update, hour=[0], minute=[0], second=[1] )

        
    def update(self, now):
        """Get the latest data and updates the states."""

        params = {
            "key": self.key,
            "page": randint(1,25000),
            "pagesize": 20
            }

        f = request.urlopen( self.url, parse.urlencode(params).encode('utf-8') )

        content = f.read()
        
        result = json.loads(content.decode('utf-8'))

        if result is None:
            _LOGGER.error("Request api Error")
            return
        elif (result["error_code"] != 0):
            _LOGGER.error("Error API return, errorcode=%s, reson=%s",
                          result["error_code"],
                          result["reason"],
                          )
            return
        
        self.story = {}
        i = 0
        for data in result["result"]["data"]:
            i = i+1
            self.story["story%d" %(i)] = data["content"]
            
        self.state = 'ready'

