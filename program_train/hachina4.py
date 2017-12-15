"""
文件名 hachina.py.

演示程序，读取配置文件的内容.
"""

import logging
# 引入这两个库，用于配置文件格式校验
import voluptuous as vol
import homeassistant.helpers.config_validation as cv

DOMAIN = "hachina"
ENTITYID = DOMAIN + ".hello_world"

# 预定义配置文件中的key值
CONF_NAME_TOBE_DISPLAYED = "name_tobe_displayed"
CONF_SLOGON = "slogon"

# 预定义缺省的配置值
DEFAULT_SLOGON = "积木构建智慧空间！"

_LOGGER = logging.getLogger(__name__)

# 配置文件的样式
CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                # “name_tobe_displayed”在配置文件中是必须存在的（Required），否则报错，它的类型是字符串
                vol.Required(CONF_NAME_TOBE_DISPLAYED): cv.string,
                # “slogon”在配置文件中可以没有（Optional），如果没有缺省值为“积木构建智慧空间！”，它的类型是字符串
                vol.Optional(CONF_SLOGON, default=DEFAULT_SLOGON): cv.string,
            }),
    },
    extra=vol.ALLOW_EXTRA)


def setup(hass, config):
    """配置文件加载后，setup被系统调用."""
    # config[DOMAIN]代表这个域下的配置信息
    conf = config[DOMAIN]
    # 获得具体配置项信息
    friendly_name = conf.get(CONF_NAME_TOBE_DISPLAYED)
    slogon = conf.get(CONF_SLOGON)

    _LOGGER.info("Get the configuration %s=%s; %s=%s",
                 CONF_NAME_TOBE_DISPLAYED, friendly_name,
                 CONF_SLOGON, slogon)

    # 根据配置内容设置属性值
    attr = {"icon": "mdi:yin-yang",
            "friendly_name": friendly_name,
            "slogon": slogon}
    hass.states.set(ENTITYID, '太棒了', attributes=attr)

    return True
