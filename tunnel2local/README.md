
## 说明：
 - 本组件使用[frp](https://github.com/fatedier/frp)作为建立隧道的工具
 - 本组件仅实现了http虚拟主机，用于在INTERNET上访问homeassistant开放的端口
 
 
## frp下载地址：
https://github.com/fatedier/frp/releases


## 使用：
 - 将`tunnel2local.py`放置在`~/.homeassistant/custom_components/`目录下
 - 配置文件：
 
```yaml
tunnel2local:
  # frpc命令位置
  # frpc_bin: "C:/local/frp_0.16.0_windows_amd64/frpc.exe"
  # frp服务器IP地址或主机名
  # frps: "1.2.3.4"
  # frp服务端口
  # frps_port: 7000
  # frp privilege_token
  # frp_privilege_token: ""
  # 注册的主机服务域名
  # subdomain: abcd123
```
