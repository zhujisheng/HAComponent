"""
文件名 hachina.py.

演示程序，注册一个服务.
"""

# 引入记录日志的库
import logging

DOMAIN = "hachina"
ENTITYID = DOMAIN + ".hello_world"

# 在python中，__name__代表模块名字
_LOGGER = logging.getLogger(__name__)


def setup(hass, config):
    """配置文件加载后，setup被系统调用."""
    attr = {"icon": "mdi:yin-yang",
            "friendly_name": "迎接新世界",
            "slogon": "积木构建智慧空间！", }
    hass.states.set(ENTITYID, '太棒了', attributes=attr)

    def change_state(call):
        """change_state函数切换改变实体的状态."""
        # 记录info级别的日志
        _LOGGER.info("hachina's change_state service is called.")

        # 切换改变状态值
        if hass.states.get(ENTITYID).state == '太棒了':
            hass.states.set(ENTITYID, '真好', attributes=attr)
        else:
            hass.states.set(ENTITYID, '太棒了', attributes=attr)

    # 注册服务hachina.change_state
    hass.services.register(DOMAIN, 'change_state', change_state)

    return True
