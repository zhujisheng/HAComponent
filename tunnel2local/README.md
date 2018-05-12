
## 说明：
 - 本组件使用[frp](https://github.com/fatedier/frp)作为建立隧道的工具
 - 本组件基于域名hachina.802154.com的http虚拟主机头，实现在INTERNET上访问homeassistant开放的端口
 - 自己搭建frp服务器端，也可以使用本组件，以tcp转发方式实现内网homeassistant的外网访问
 
 
## 下载frp：
https://github.com/fatedier/frp/releases

找到您homeassistant所在的操作系统，下载对应的文件。
**我们仅需要其中的frpc程序。**
**目前服务器端为0.18.0版，因此请下载对应客户端版本**

如果是树莓派，使用`frp_0.18.0_linux_arm.tar.gz`，解压缩后获得frpc文件（可能需要增加可执行权限`chmod +x frpc`），在下面的配置文件中配置其地址。


## 配置HomeAssistant：
 - （适用于python3.5环境用户）将`tunnel2local.pyc`与`tunnel2local.xx`放置在`~/.homeassistant/custom_components/`目录下
 - （python3.6环境用户）下载`tunnel2local.cpython-36.pyc`，改名成`tunnel2local.pyc`；改名后的文件与`tunnel2local.xx`放置在`~/.homeassistant/custom_components/`目录下
 - 配置文件：
 ```yaml
tunnel2local:
  # frpc命令位置
  frpc_bin: "C:/local/frp_0.18.0_windows_amd64/frpc.exe"

```
## （可选）搭建自己的frp服务器
如果您选择搭建自己的frp服务器，参见：[server_diy.md](server_diy.md)
