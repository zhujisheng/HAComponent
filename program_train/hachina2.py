"""
文件名 hachina.py.

演示程序，增加设备的属性值.
"""

# HomeAssistant的惯例，会在组件程序中定义域，域与组件程序名相同
DOMAIN = "hachina"


def setup(hass, config):
    """配置文件加载后，被调用的程序."""
    # 准备一些属性值，在给实体设置状态的同时，设置实体的这些属性
    attr = {"icon": "mdi:yin-yang",
            "friendly_name": "迎接新世界",
            "slogon": "积木构建智慧空间！"}

    # 使用了在程序开头预定义的域
    # 设置状态的同时，设置实体的属性
    hass.states.set(DOMAIN+".hello_world", "太棒了！", attributes=attr)
    return True
