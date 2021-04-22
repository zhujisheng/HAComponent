*本组件使用chrome浏览器访问页面获得内容后，使用beautiful soap selector获得其中的元素。*

## 配置

*可以参见官方的[scrape集成](https://www.home-assistant.io/integrations/scrape/)的配置；两者配置方式相同，仅获取网页的方式不同*

```yaml
# configuration.yaml样例
sensor:
  - platform: scrape2
    name: HA最新版本号
    resource: https://www.home-assistant.io
    select: ".current-version h1"
    value_template: '{{ value.split(":")[1] }}'
```

## 自定义组件安装

- `sensor.py` `__init__.py` `manifest.json`文件放置在`.homeassistant/custom_components/scrape2/`目录中
- 安装chromedriver和chrome浏览器


## 安装chromedriver和chrome浏览器

- 以docker方式运行的HomeAssistant（包括hassio和hassos方式安装的HomeAssistant）

    进入homeassistant docker后，运行

    `apk add chromium-chromedriver`

    `apk add chromium`

    如果是在中国境内，可以先运行以下命令，设置apk安装国内镜像：

    `sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories`


- 树莓派上非docker方式运行的HomeAssistant

    [树莓派对应下载地址](https://launchpad.net/ubuntu/trusty/armhf/chromium-chromedriver/65.0.3325.181-0ubuntu0.14.04.1)

    下载后运行：

    `sudo dpkg -i chromium-chromedriver_65.0.3325.181-0ubuntu0.14.04.1_armhf.deb`
