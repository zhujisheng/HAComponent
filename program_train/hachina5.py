"""
文件名 hachina.py.

演示程序，事件触发状态值的改变.
"""

# 引入datetime库用于方便时间相关计算
from datetime import timedelta
import logging
import voluptuous as vol

# 引入HomeAssitant中定义的一些类与函数
# track_time_interval是监听时间变化事件的一个函数
from homeassistant.helpers.event import track_time_interval
import homeassistant.helpers.config_validation as cv


DOMAIN = "hachina"
ENTITYID = DOMAIN + ".hello_world"

CONF_STEP = "step"
DEFAULT_STEP = 3

# 定义时间间隔为3秒钟
TIME_BETWEEN_UPDATES = timedelta(seconds=3)

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                # 一个配置参数“step”，只能是正整数，缺省值为3
                vol.Optional(CONF_STEP, default=DEFAULT_STEP): cv.positive_int,
            }),
    },
    extra=vol.ALLOW_EXTRA)


def setup(hass, config):
    """配置文件加载后，setup被系统调用."""
    conf = config[DOMAIN]
    step = conf.get(CONF_STEP)

    _LOGGER.info("Get the configuration %s=%d",
                 CONF_STEP, step)

    attr = {"icon": "mdi:yin-yang",
            "friendly_name": "迎接新世界",
            "slogon": "积木构建智慧空间！",
            "unit_of_measurement": "steps"}

    # 构建类GrowingState
    GrowingState(hass, step, attr)

    return True


class GrowingState(object):
    """定义一个类，此类中存储了状态与属性值，并定时更新状态."""

    def __init__(self, hass, step, attr):
        """GrwoingState类的初始化函数，参数为hass、step和attr."""
        # 定义类中的一些数据
        self._hass = hass
        self._step = step
        self._attr = attr
        self._state = 0

        # 在类初始化的时候，设置初始状态
        self._hass.states.set(ENTITYID, self._state, attributes=self._attr)

        # 每隔一段时间，更新一下实体的状态
        track_time_interval(self._hass, self.update, TIME_BETWEEN_UPDATES)

    def update(self, now):
        """在GrowingState类中定义函数update,更新状态."""
        _LOGGER.info("GrowingState is updating…")

        # 状态值每次增加step
        self._state = self._state + self._step

        # 设置新的状态值
        self._hass.states.set(ENTITYID, self._state, attributes=self._attr)
