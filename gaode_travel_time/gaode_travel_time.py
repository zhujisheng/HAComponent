"""
Support for Gaode travel time sensors.

by HAChina
"""
import http.client
from urllib.parse import quote
from datetime import timedelta
import logging
import json

import voluptuous as vol

from homeassistant.components.sensor import (DOMAIN, PLATFORM_SCHEMA)
from homeassistant.helpers.entity import Entity
from homeassistant.const import (
    ATTR_ATTRIBUTION, CONF_API_KEY )
#from homeassistant.util import Throttle
from homeassistant.helpers.event import track_time_interval
import homeassistant.helpers.config_validation as cv
import homeassistant.util.dt as dt_util



_LOGGER = logging.getLogger(__name__)


CONF_ORIGIN = 'origin'
CONF_DESTINATION = 'destination'
CONF_TRAVEL_MODE = 'travel_mode'
CONF_STRATEGY = 'strategy'
CONF_ATTRIBUTION = "Transport information provided by Gaode"
CONF_LONGITUDE_LATITUDE = "longitude_latitude"
CONF_CITY = "city"
CONF_ADDRESS = "address"
CONF_NAME = "name"
CONF_FRIENDLY_NAME = 'friendly_name'

DEFAULT_NAME = 'Gaode Travel Time'
DEFAULT_TRAVEL_MODE = 'driving'
DEFAULT_STRATEGY = 0

TIME_BETWEEN_UPDATES = timedelta(minutes=30)


TRAVEL_MODE = ['driving', 'walking', 'bicycling']

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_API_KEY): cv.string,
    vol.Required(CONF_ORIGIN): vol.All(dict, vol.Schema({
        vol.Optional(CONF_LONGITUDE_LATITUDE): cv.string,
        vol.Optional(CONF_CITY):cv.string,
        vol.Optional(CONF_ADDRESS):cv.string,
        })),
    vol.Required(CONF_DESTINATION): vol.All(dict, vol.Schema({
        vol.Optional(CONF_LONGITUDE_LATITUDE): cv.string,
        vol.Optional(CONF_CITY):cv.string,
        vol.Optional(CONF_ADDRESS):cv.string,
        })),
    vol.Optional(CONF_NAME, default= DEFAULT_NAME): cv.string,
    vol.Optional(CONF_FRIENDLY_NAME, default= DEFAULT_NAME): cv.string,
    vol.Optional(CONF_TRAVEL_MODE, default=DEFAULT_TRAVEL_MODE): vol.In(TRAVEL_MODE),
    vol.Optional(CONF_STRATEGY,default=DEFAULT_STRATEGY):vol.All(vol.Coerce(int), vol.Range(min=0,max=9)),
    })




def setup_platform(hass, config, add_devices, discovery_info=None):

        api_key = config.get(CONF_API_KEY)
        origin = config.get(CONF_ORIGIN)
        destination = config.get(CONF_DESTINATION)
        travel_mode = config.get(CONF_TRAVEL_MODE)
        strategy = config.get(CONF_STRATEGY)

        name = config.get(CONF_NAME)
        friendly_name = config.get(CONF_FRIENDLY_NAME)

        data = GaodeTravelTimeData( hass, api_key, origin, destination, travel_mode, strategy )

        sensor = GaodeTravelTimeSensor( hass, name, friendly_name, data )

        add_devices([sensor])

        def update(call=None):
                '''Update the data by service call'''
                data.update(dt_util.now())
                sensor.update()

        hass.services.register(DOMAIN, name+'_update', update)



class GaodeTravelTimeSensor(Entity):
    """Representation of a Gaode travel time sensor."""

    def __init__(self, hass, name, friendly_name, data ):
        """Initialize the sensor."""
        self._hass = hass
        self._name = name
        self._friendly_name = friendly_name
        self._unit_of_measurement = "分钟"
        self._data = data



    @property
    def state(self):
        """Return the state of the sensor."""
        return self._data._duration

    @property
    def name(self):
        """Get the name of the sensor."""
        return self._name

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        if self._data is not None:
            return {
                ATTR_ATTRIBUTION: CONF_ATTRIBUTION,
                CONF_ORIGIN:self._data._origin,
                CONF_DESTINATION:self._data._destination,
                CONF_TRAVEL_MODE:self._data._travel_mode,
                CONF_STRATEGY:self._data._strategy,
                CONF_FRIENDLY_NAME:self._friendly_name,
                "distance":self._data._distance,
                "textguide": self._data._textguide,
                "update_time": self._data._update_time
                }


    @property
    def unit_of_measurement(self):
        """Return the unit this state is expressed in."""
        return self._unit_of_measurement

    #@Throttle(TIME_BETWEEN_UPDATES)
    def update(self):
        """Get the latest data from Google."""
        #self._data.update()______________________????????????????????




class GaodeTravelTimeData(Entity):
    """Representation of a Gaode Travel Time sensor"""

    def __init__(self, hass, api_key, origin, destination, travel_mode, strategy ):
        
        self._host = 'restapi.amap.com'

        self._duration = None
        self._distance = None
        self._textguide = None
        self._origin = None
        self._destination = None
        self._travel_mode = travel_mode
        self._strategy = None
        self._api_key = api_key
        self._update_time = None
        
        
        origin_longitude_latitude = self.get_longitude_latitude(origin)
        destination_longitude_latitude = self.get_longitude_latitude(destination)

        if( travel_mode == "walking" ):
            self._url = ( '/v3/direction/walking?key='
                          + api_key
                          + '&origin=' + origin_longitude_latitude
                          + '&destination=' + destination_longitude_latitude
                          + '&output=JSON'
                          )
        elif( travel_mode == "bicycling"):
            self._url = ( '/v4/direction/bicycling?key='
                          + api_key
                          + '&origin=' + origin_longitude_latitude
                          + '&destination=' + destination_longitude_latitude
                          )
        else:
            self._url = ( '/v3/direction/driving?key='
                          + api_key
                          + '&origin=' + origin_longitude_latitude
                          + '&destination=' + destination_longitude_latitude
                          + '&extensions=base'
                          + '&strategy=' + str(strategy)
                          + '&output=JSON'
                          )
            
        self.update(dt_util.now())
        track_time_interval( hass, self.update, TIME_BETWEEN_UPDATES )



        
    def update(self, now):
        
        conn = http.client.HTTPConnection(self._host)
        conn.request("GET",self._url)
        result = conn.getresponse()

        if(result.status != 200):
            _LOGGER.error("Error http reponse: %d", result.status)

        data = json.loads( str(result.read(),encoding = 'utf-8') )

        if(self._travel_mode != "bicycling"):
            if(data['status'] != '1'):
                _LOGGER.error("Error Api return, state=%s, errmsg=%s",
                              data['status'],
                              data['info']
                              )
                return

            dataroute = data["route"]

            
        else:
            if(data['errcode'] != 0 ):
                _LOGGER.error("Error Api return, errcode=%s, errmsg=%s",
                              data['errcode'],
                              data['errmsg'],
                              )
                return
            dataroute = data['data']
                    

        self._origin = dataroute["origin"]
        self._destination = dataroute["destination"]
        if(self._travel_mode == "driving"):
            self._strategy = dataroute["paths"][0]["strategy"]
        
        self._duration = int(dataroute["paths"][0]["duration"])/60
        self._distance = float(dataroute["paths"][0]["distance"])/1000

        bypasstext = "途经"
        roadbefore = ""
        for step in dataroute["paths"][0]["steps"]:
            if ('road' in step.keys() and step["road"] != []):
                if( step["assistant_action"] == "到达目的地" ):
                    if (step["road"] != roadbefore):
                        bypasstext = bypasstext + roadbefore + step["road"] + "。"
                        roadbefore = step["road"]
                    else:
                        bypasstext = bypasstext + roadbefore + "。"
                        roadbefore = step["road"]
                else:
                    if roadbefore == "":
                        roadbefore = step["road"]
                    elif (step["road"] != roadbefore):
                        bypasstext = bypasstext + roadbefore + "、"
                        roadbefore = step["road"]
        
        self._textguide = ("距离%.1f公里。需花时%d分钟。%s"
                           %(self._distance,
                             self._duration,
                             bypasstext
                             )
                          )
        self._update_time = dt_util.now()

    def get_longitude_latitude(self, address_dict):
            
        if address_dict.get(CONF_LONGITUDE_LATITUDE) is not None:
            return address_dict.get(CONF_LONGITUDE_LATITUDE)

        if (address_dict.get(CONF_ADDRESS) is None) or (address_dict.get(CONF_CITY) is None):
            return
            
        url = ("/v3/geocode/geo?key="
               + self._api_key
               + '&address=' + address_dict.get(CONF_ADDRESS)
               + '&city=' + address_dict.get(CONF_CITY)
               )

        conn = http.client.HTTPConnection(self._host)
        conn.request("GET",quote(url, safe='/:?=&'))
        result = conn.getresponse()

        if(result.status != 200):
            _LOGGER.error("Error http reponse: %d", result.status)

        data = json.loads( str(result.read(),encoding = 'utf-8') )
        if(data['status'] != '1'):
            _LOGGER.error("Error Api return, state=%s, errmsg=%s",
                          data['status'],
                          data['info']
                          )
            return

        return data['geocodes'][0]['location']
            

