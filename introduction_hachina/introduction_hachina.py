"""

For more details about HAChina,
https://www.hachina.io/
"""
import asyncio
import logging

import voluptuous as vol

DOMAIN = 'introduction'

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({}),
}, extra=vol.ALLOW_EXTRA)


@asyncio.coroutine
def async_setup(hass, config=None):
    """Set up the introduction component."""
    log = logging.getLogger(__name__)
    log.info("""

    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        欢迎使用HACHINA.IO创建的镜像文件！

        我们的网站https://www.hachina.io


        This message is generated by the introduction_hachina component. You can
        disable it in configuration.yaml.

    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """)

    hass.components.persistent_notification.async_create("""
[![HACHINA](https://www.hachina.io/wp-content/themes/haChina/images/logo@2x.png)](https://www.hachina.io)

在此镜像文件中，我们安装与开放了以下服务:

 - [HomeAssistant](https://home-assistant.io/)
 - [Jupyter Notebook](http://jupyter.org/)
 - [Mosquitto](http://www.mosquitto.org/)
 - [Samba](https://www.samba.org/)
 - [SshD](https://www.openssh.com/)
 - [AppDaemon&DashBoard](https://appdaemon.readthedocs.io/)
 
密码与修改:

 - 操作系统的`pi`账号，初始密码为`hachina`。以`pi`账号登录后，使用`passwd`命令修改
 - HomeAssistant的未设置API密码（Legacy API Password）
 - Jupyter Notebook的初始访问密码为`hachina`。以`pi`账号登录后，使用`jupyter notebook password`命令修改
 - Mosquitto的用户名为`pi`，初始密码为`hachina`。以`pi`账号登录后，使用`sudo mosquitto_passwd /etc/mosquitto/passwd pi`命令修改
 - DashBoard的初始访问密码为`hachina`（访问端口为5050）。以`pi`账号登录后，在文件`/home/pi/appdaemon/appdaemon.yaml`中修改。

第一次启动，HomeAssistant会自动生成配置文件，与标准的HomeAssistant缺省配置比较，有以下不同：

 - 配置目录下空白的`known_devices.yaml`文件
 - 配置来自自身（127.0.0.1）的访问不需要认证trusted_networks
 - 配置在sensor组件下的bitcoin平台
 - 将tts组件中google平台设置为中文
 - 媒体播放器（media_player）组件中配置vlc平台
 - [introduction_hachina组件](https://github.com/zhujisheng/HAComponent/tree/master/introduction_hachina)
 - [tunnel2local组件](https://github.com/zhujisheng/HAComponent/tree/master/tunnel2local)
 - [redpoint组件](https://github.com/HAChina/redpoint)

 
我们的网站：[https://www.hachina.io](https://www.hachina.io)

欲去除本卡信息，请编辑`configuration.yaml`文件，删除或注释调`introduction_hachina`组件
""", '欢迎使用HACHINA.IO创建的镜像文件！')  # noqa

    return True
