
## 说明：
 - 本组件使用[frp](https://github.com/fatedier/frp)作为建立隧道的工具
 - 本组件基于域名hachina.802154.com的http虚拟主机头，实现在INTERNET上访问homeassistant开放的端口
 - 自己搭建frp服务器端，也可以使用本组件，以tcp转发方式实现内网homeassistant的外网访问
 
 
## 下载frp：
https://github.com/fatedier/frp/releases

找到您homeassistant所在的操作系统，下载对应的文件。

**我们仅需要其中的frpc程序。**

**缺省的服务器端为0.18.0版。如果你使用缺省服务器，请下载对应客户端版本；如果你自己搭建服务器端，服务器端与客户端版本一致即可**

**缺省服务器端仅供测试使用，流量较大，网络质量不好；建议自己搭建服务器端**

例如：如果是树莓派，如果要使用0.18版本，对应文件为`frp_0.18.0_linux_arm.tar.gz`，解压缩后获得frpc文件（可能需要增加可执行权限`chmod +x frpc`），在下面的配置文件中配置其地址。


## 配置HomeAssistant：
 - 在`~/.homeassistant/custom_components/`目录下构建子目录`tunnel2local`
 - 下载文件`__init__.py`与`manifest.json`，放置在目录`tunnel2local`中
 - 配置文件：

```yaml
tunnel2local:
  # frpc命令位置
  frpc_bin: "C:/local/frp_0.18.0_windows_amd64/frpc.exe"

```
## （可选）搭建自己的frp服务器
如果您选择搭建自己的frp服务器，参见：[server_diy.md](server_diy.md)
