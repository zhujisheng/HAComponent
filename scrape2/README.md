本组件使用chrome浏览器访问页面获得内容后，使用beautiful soap selector获得其中的元素。

<br>
<br>

`chromedriver`文件预先放置在`/usr/lib/chromium-browser`目录中。

[树莓派对应下载地址](https://launchpad.net/ubuntu/trusty/armhf/chromium-chromedriver/65.0.3325.181-0ubuntu0.14.04.1)

下载后运行：

`sudo dpkg -i chromium-chromedriver_65.0.3325.181-0ubuntu0.14.04.1_armhf.deb`
<br>
**`sensor.py`文件放置在`.homeassistant/custom_components/scrape2/`目录中。
**
<br>
<br>

将以下内容放置在`configuration.yaml`文件中：
```yaml
# configuration.yaml样例
sensor:
  - platform: scrape2
    name: HA最新版本号
    resource: https://www.home-assistant.io
    select: ".current-version h1"
    value_template: '{{ value.split(":")[1] }}'
```
