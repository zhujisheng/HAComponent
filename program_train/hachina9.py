"""
文件名：hachina.py.

文件位置：HomeAssistant配置目录/custom_components/sensor/hachina.py
演示程序，异步工作的平台程序.

"""

import logging
from datetime import timedelta

# 此处引入了几个异步处理的库
import asyncio
import async_timeout
import aiohttp

import voluptuous as vol

# aiohttp_client将aiohttp的session与hass关联起来
# track_time_interval需要使用对应的异步的版本
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.event import async_track_time_interval

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (
    ATTR_ATTRIBUTION, ATTR_FRIENDLY_NAME, TEMP_CELSIUS)
from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv
import homeassistant.util.dt as dt_util


_LOGGER = logging.getLogger(__name__)

TIME_BETWEEN_UPDATES = timedelta(seconds=600)

CONF_OPTIONS = "options"
CONF_CITY = "city"
CONF_APPKEY = "appkey"

# 定义三个可选项：温度、湿度、PM2.5
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
    vol.Required(CONF_OPTIONS,
                 default=[]): vol.All(cv.ensure_list, [vol.In(OPTIONS)]),
})


@asyncio.coroutine
def async_setup_platform(hass, config, async_add_devices, discovery_info=None):
    """这个协程是程序的入口，其中add_devices函数也变成了异步版本."""
    _LOGGER.info("setup platform sensor.hachina...")

    city = config.get(CONF_CITY)
    appkey = config.get(CONF_APPKEY)

    data = WeatherData(hass, city, appkey)
    # 大家可以尝试把yield from去除，看看是什么效果（参见知识点小结）
    yield from data.async_update(dt_util.now())
    async_track_time_interval(hass, data.async_update, TIME_BETWEEN_UPDATES)

    # 根据配置文件options中的内容，添加若干个设备
    dev = []
    for option in config[CONF_OPTIONS]:
        dev.append(HAChinaWeatherSensor(data, option))
    async_add_devices(dev, True)


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

    @asyncio.coroutine
    def async_update(self):
        """update函数变成了async_update."""
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
        self._hass = hass

        self._url = "https://way.jd.com/he/freeweather"
        self._params = {"city": city,
                        "appkey": appkey}
        self._temprature = None
        self._humidity = None
        self._pm25 = None
        self._updatetime = None

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

    @asyncio.coroutine
    def async_update(self, now):
        """从远程更新信息."""
        _LOGGER.info("Update from JingdongWangxiang's OpenAPI...")

        """
        # 异步模式的测试代码
        import time
        _LOGGER.info("before time.sleep")
        time.sleep(40)
        _LOGGER.info("after time.sleep and before asyncio.sleep")
        asyncio.sleep(40)
        _LOGGER.info("after asyncio.sleep and before yield from asyncio.sleep")
        yield from asyncio.sleep(40)
        _LOGGER.info("after yield from asyncio.sleep")
        """

        # 通过HTTP访问，获取需要的信息
        # 此处使用了基于aiohttp库的async_get_clientsession
        try:
            session = async_get_clientsession(self._hass)
            with async_timeout.timeout(15, loop=self._hass.loop):
                response = yield from session.post(
                    self._url, data=self._params)

        except(asyncio.TimeoutError, aiohttp.ClientError):
            _LOGGER.error("Error while accessing: %s", self._url)
            return

        if response.status != 200:
            _LOGGER.error("Error while accessing: %s, status=%d",
                          self._url,
                          response.status)
            return

        try:
            result = yield from response.json()
        except(aiohttp.client_exceptions.ContentTypeError):
            _LOGGER.error("Error return type: %s", str(response))
            return

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
