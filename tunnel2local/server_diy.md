如果您不想使用组件中现成的公网隧道，可以使用frp自己搭建服务器端——前提条件是：您有一台公网能直接访问到的服务器（云主机）。


## 服务器端搭建
使用下载的frp包中的frps程序，在服务器上运行。配置文件`frps.ini`如下：
```ini
[common]
bind_port = 7000
token = 12345678
```
其余的配置项可以参见frps项目的配置说明

## HomeAssistant配置
 - 如[readme](https://github.com/zhujisheng/HAComponent/tree/master/tunnel2local)中所述，安放`tunnel2local.pyc`和`tunnel2local.xx`文件
 - 配置文件：
 ```yaml
tunnel2local:
  # frpc命令位置
  frpc_bin: "C:/local/frp_0.18.0_windows_amd64/frpc.exe"
  frps: 1.2.3.4   #服务器地址
  frps_port: 7000  #缺省值为7000
  frp_token: "12345678"  #缺省值为空
  remote_port: 8123  #缺省值为8123

```
