"""
The chinese stock market price information comes from Aliyun.

by HAChina.io

"""
import logging
import asyncio
from datetime import timedelta

import voluptuous as vol
import http.client

import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import ATTR_ATTRIBUTION
from homeassistant.helpers.entity import Entity


_LOGGER = logging.getLogger(__name__)

ATTR_OPEN = 'open'
ATTR_PREV_CLOSE = 'prev_close'
ATTR_HIGH = 'high'
ATTR_LOW = 'low'
ATTR_NAME = 'friendly_name'

CONF_ATTRIBUTION = "Chinese stock market information provided by Aliyun"
CONF_SYMBOLS = 'symbols'
CONF_APPCODE = 'appcode'


DEFAULT_SYMBOL = 'sz000002'

ICON = 'mdi:currency-cny'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_SYMBOLS, default=[DEFAULT_SYMBOL]):
        vol.All(cv.ensure_list, [cv.string]),
    vol.Required(CONF_APPCODE):cv.string,
})

@asyncio.coroutine
def async_setup_platform(hass, config, async_add_devices, discovery_info=None):
    """Set up the Aliyun_stock sensor."""

    symbols = config.get(CONF_SYMBOLS)
    appcode = config.get(CONF_APPCODE)

    dev = []
    for symbol in symbols:
        data = AliyunStockData(hass, symbol, appcode)
        dev.append(AliyunStockSensor(data, symbol))

    async_add_devices(dev, True)


class AliyunStockSensor(Entity):
    """Representation of a Aliyun Stock sensor."""

    def __init__(self, data, symbol):
        """Initialize the sensor."""
        self.data = data
        self._symbol = symbol
        self._state = None
        self._unit_of_measurement = '元'
        self._name = symbol

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this entity, if any."""
        return self._unit_of_measurement

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        if self._state is not None:
            return {
                ATTR_ATTRIBUTION: CONF_ATTRIBUTION,
                ATTR_OPEN: self.data.price_open,
                ATTR_PREV_CLOSE: self.data.prev_close,
                ATTR_HIGH: self.data.high,
                ATTR_LOW: self.data.low,
                ATTR_NAME: self.data.name,
            }

    @property
    def icon(self):
        """Return the icon to use in the frontend, if any."""
        return ICON
    
    @asyncio.coroutine
    def async_update(self):
        """Get the latest data and updates the states."""
        _LOGGER.debug("Updating sensor %s - %s", self._name, self._state)
        self.data.update()
        self._state = self.data.state


class AliyunStockData(object):
    """Get data from Aliyun stock imformation."""

    def __init__(self, hass, symbol, appcode):
        """Initialize the data object."""


        self._symbol = symbol
        self.state = None
        self.price_open = None
        self.prev_close = None
        self.high = None
        self.low = None
        self.name = None
        self.hass = hass

        self.host = 'ali.api.intdata.cn'
        self.url = "/stock/hs_level2/real?code=" + self._symbol
        self.head = {
            "Authorization":"APPCODE "+ appcode,
            }

        
    def update(self):
        """Get the latest data and updates the states."""
        conn = http.client.HTTPConnection(self.host)
        conn.request("GET",self.url,headers=self.head)
        result = conn.getresponse()

        if(result.status != 200):
            _LOGGER.error("Error http reponse: %d", result.status)

        data = eval(result.read())

        if(data['state'] != 0):
            _LOGGER.error("Error Api return, state=%d, errmsg=%s",
                          data['state'],
                          data['errmsg']
                          )
            return

        self.state = data['data']['price']
        self.high = data['data']['high']
        self.low = data['data']['low']
        self.price_open = data['data']['open']
        self.prev_close = data['data']['last_close']
        self.name = data['data']['name']
