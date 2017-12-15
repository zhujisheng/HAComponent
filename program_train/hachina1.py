"""
文件名：hachina.py.

演示程序，三行代码创建一个新设备.
"""


def setup(hass, config):
    """HomeAssistant在配置文件中发现hachina域的配置后，会自动调用hachina.py文件中的setup函数."""
    # 设置实体hachina.Hello_World的状态。
    # 注意1：实体并不需要被创建，只要设置了实体的状态，实体就自然存在了
    # 注意2：实体的状态可以是任何字符串
    hass.states.set("hachina.hello_world", "太棒了！")

    # 返回True代表初始化成功
    return True
