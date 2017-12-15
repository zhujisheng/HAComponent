"""
文件名：hachina.py.

文件位置：HomeAssistant配置目录/custom_components/sensor/hachina.py
演示程序，一个平台实现多个传感器.

"""

import json
from urllib import request, parse
import logging
from datetime import timedelta
import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (
    ATTR_ATTRIBUTION, ATTR_FRIENDLY_NAME, TEMP_CELSIUS)
from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.event import track_time_interval
import homeassistant.util.dt as dt_util


_LOGGER = logging.getLogger(__name__)

TIME_BETWEEN_UPDATES = timedelta(seconds=600)

# 配置文件中三个配置项的名称
CONF_OPTIONS = "options"
CONF_CITY = "city"
CONF_APPKEY = "appkey"

# 定义三个可选项：温度、湿度、PM2.5
# 格式：配置项名称:[OBJECT_ID, friendly_name, icon, 单位]
OPTIONS = {
    "temprature": [
        "hachina_temperature", "室外温度", "mdi:thermometer", TEMP_CELSIUS],
    "humidity": ["hachina_humidity", "室外湿度", "mdi:water-percent", "%"],
    "pm25": ["hachina_pm25", "PM2.5", "mdi:walk", "μg/m3"],
}

ATTR_UPDATE_TIME = "更新时间"
ATTRIBUTION = "来自京东万象的天气数据"


PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_CITY): cv.string,
    vol.Required(CONF_APPKEY): cv.string,
    # 配置项的options是一个列表，列表内容只能是OPTIONS中定义的三个可选项
    vol.Required(CONF_OPTIONS,
                 default=[]): vol.All(cv.ensure_list, [vol.In(OPTIONS)]),
})


def setup_platform(hass, config, add_devices, discovery_info=None):
    """根据配置文件，setup_platform函数会自动被系统调用."""
    _LOGGER.info("setup platform sensor.hachina...")

    city = config.get(CONF_CITY)
    appkey = config.get(CONF_APPKEY)

    # 定义一个新的数据对象，用于从京东万象获取并存储天气数据。Sensor的实际数据从这个对象中获得。
    data = WeatherData(hass, city, appkey)

    # 根据配置文件options中的内容，添加若干个设备
    dev = []
    for option in config[CONF_OPTIONS]:
        dev.append(HAChinaWeatherSensor(data, option))
    add_devices(dev, True)


class HAChinaWeatherSensor(Entity):
    """定义一个温度传感器的类，继承自HomeAssistant的Entity类."""

    def __init__(self, data, option):
        """初始化."""
        self._data = data
        self._object_id = OPTIONS[option][0]
        self._friendly_name = OPTIONS[option][1]
        self._icon = OPTIONS[option][2]
        self._unit_of_measurement = OPTIONS[option][3]

        self._type = option
        self._state = None
        self._updatetime = None

    @property
    def name(self):
        """返回实体的名字."""
        return self._object_id

    @property
    def state(self):
        """返回当前的状态."""
        return self._state

    @property
    def icon(self):
        """返回icon属性."""
        return self._icon

    @property
    def unit_of_measurement(self):
        """返回unit_of_measuremeng属性."""
        return self._unit_of_measurement

    @property
    def device_state_attributes(self):
        """设置其它一些属性值."""
        if self._state is not None:
            return {
                ATTR_ATTRIBUTION: ATTRIBUTION,
                ATTR_FRIENDLY_NAME: self._friendly_name,
                ATTR_UPDATE_TIME: self._updatetime
            }

    def update(self):
        """更新函数，在sensor组件下系统会定时自动调用（时间间隔在配置文件中可以调整，缺省为30秒）."""
        # update只是从WeatherData中获得数据，数据由WeatherData维护。
        self._updatetime = self._data.updatetime

        if self._type == "temprature":
            self._state = self._data.temprature
        elif self._type == "humidity":
            self._state = self._data.humidity
        elif self._type == "pm25":
            self._state = self._data.pm25


class WeatherData(object):
    """天气相关的数据，存储在这个类中."""

    def __init__(self, hass, city, appkey):
        """初始化函数."""
        self._url = "https://way.jd.com/he/freeweather"
        self._params = {"city": city,
                        "appkey": appkey}
        self._temprature = None
        self._humidity = None
        self._pm25 = None
        self._updatetime = None

        self.update(dt_util.now())
        # 每隔TIME_BETWEEN_UPDATES，调用一次update(),从京东万象获取数据
        track_time_interval(hass, self.update, TIME_BETWEEN_UPDATES)

    @property
    def temprature(self):
        """温度."""
        return self._temprature

    @property
    def humidity(self):
        """湿度."""
        return self._humidity

    @property
    def pm25(self):
        """pm2.5."""
        return self._pm25

    @property
    def updatetime(self):
        """更新时间."""
        return self._updatetime

    def update(self, now):
        """从远程更新信息."""
        _LOGGER.info("Update from JingdongWangxiang's OpenAPI...")

        # 通过HTTP访问，获取需要的信息
        infomation_file = request.urlopen(
            self._url, parse.urlencode(self._params).encode('utf-8'))

        content = infomation_file.read()
        result = json.loads(content.decode('utf-8'))

        if result is None:
            _LOGGER.error("Request api Error")
            return
        elif result["code"] != "10000":
            _LOGGER.error("Error API return, code=%s, msg=%s",
                          result["code"],
                          result["msg"])
            return

        # 根据http返回的结果，更新数据
        all_result = result["result"]["HeWeather5"][0]
        self._temprature = all_result["now"]["tmp"]
        self._humidity = all_result["now"]["hum"]
        self._pm25 = all_result["aqi"]["city"]["pm25"]
        self._updatetime = all_result["basic"]["update"]["loc"]
