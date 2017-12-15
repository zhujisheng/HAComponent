"""
文件名：hachina.py.

文件位置：HomeAssistant配置目录/custom_components/sensor/hachina.py
演示程序，构建一个真正的温度传感器.

"""

# 因为京东万象的数据是以http方式提供的json数据，所以引入一些处理的库
import json
from urllib import request, parse

import logging
import voluptuous as vol

# 引入sensor下的PLATFORM_SCHEMA
from homeassistant.components.sensor import PLATFORM_SCHEMA

from homeassistant.const import (
    ATTR_ATTRIBUTION, ATTR_FRIENDLY_NAME, TEMP_CELSIUS)
from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

# 配置文件中平台下的两个配置项
CONF_CITY = "city"
CONF_APPKEY = "appkey"

ATTR_UPDATE_TIME = "更新时间"

OBJECT_ID = "hachina_temperature"
ICON = "mdi:thermometer"
ATTRIBUTION = "来自京东万象的天气数据"
FRIENDLY_NAME = "当前室外温度"

# 扩展基础的SCHEMA。在我们这个platform上，城市与京东万象的APPKEY是获得温度必须要配置的项
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_CITY): cv.string,
    vol.Required(CONF_APPKEY): cv.string,
})


def setup_platform(hass, config, add_devices, discovery_info=None):
    """根据配置文件，setup_platform函数会自动被系统调用."""
    _LOGGER.info("setup platform sensor.hachina...")

    # config仅仅包含配置文件中此平台下的内容
    # 以城市与appkey作为输入参数，初始化需要的传感器对象
    sensor = HAChinaTemperatureSensor(
        config.get(CONF_CITY),
        config.get(CONF_APPKEY))

    dev = []
    dev.append(sensor)

    add_devices(dev, True)


class HAChinaTemperatureSensor(Entity):
    """定义一个温度传感器的类，继承自HomeAssistant的Entity类."""

    def __init__(self, city, appkey):
        """初始化."""
        self._state = None
        self._updatetime = None

        # 组装访问京东万象api需要的一些信息
        self._url = "https://way.jd.com/he/freeweather"
        self._params = {"city": city,
                        "appkey": appkey, }

    @property
    def name(self):
        """返回实体的名字."""
        return OBJECT_ID

    @property
    def state(self):
        """返回当前的状态."""
        return self._state

    @property
    def icon(self):
        """返回icon属性."""
        return ICON

    @property
    def unit_of_measurement(self):
        """返回unit_of_measuremeng属性."""
        return TEMP_CELSIUS

    @property
    def device_state_attributes(self):
        """设置其它一些属性值."""
        if self._state is not None:
            return {
                ATTR_ATTRIBUTION: ATTRIBUTION,
                ATTR_FRIENDLY_NAME: FRIENDLY_NAME,
                # 增加updatetime作为属性，表示温度数据的时间
                ATTR_UPDATE_TIME: self._updatetime
            }

    def update(self):
        """更新函数，在sensor组件下系统会定时自动调用（时间间隔在配置文件中可以调整，缺省为30秒）."""
        # update更新_state和_updatetime两个变量
        _LOGGER.info("Update the state...")

        # 通过HTTP访问，获取需要的信息
        infomation_file = request.urlopen(
            self._url,
            parse.urlencode(self._params).encode('utf-8'))

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

        # 根据http返回的结果，更新_state和_updatetime
        all_result = result["result"]["HeWeather5"][0]
        self._state = all_result["now"]["tmp"]
        self._updatetime = all_result["basic"]["update"]["loc"]
