此组件已经在HomeAssistant0.59版本中正式包含了。

`baidu` tts平台使用[百度tts云服务](https://cloud.baidu.com/product/speech/tts)将文字转换成语音。

将以下内容放置在`configuration.yaml`文件中：
```yaml
# configuration.yaml样例
tts:
  - platform: baidu
    app_id: YOUR_APPID
    api_key: YOUR_APIKEY
    secret_key: YOUR_SECRETKEY
    person: 4
```

可配置项：

- **app_id** （*必须项*）: 在百度云平台上登记的AppID。
- **api_key** （*必须项*）: 百度云平台上的Apikey。
- **secret_key** （*必须项*）: 百度云平台上的Secretkey。
- **speed** （*可选项*）: 语音速度，从0到9，缺省值为5。
- **pitch** （*可选项*）: 语调，从0到9，缺省值为5。
- **volume** （*可选项*）: 音量，从0到15，缺省值为5。
- **person** （*可选项*）: 可选项：0, 1, 3, 4。缺省值为0（女声）。


This component has been added to Home-Assistant since 0.59.

The `baidu` text-to-speech platform uses [Baidu TTS engine](https://cloud.baidu.com/product/speech/tts) to read a text with natural sounding voices.

To get started, add the following lines to your `configuration.yaml`:

```yaml
#Example configuration.yaml entry
tts:
  - platform: baidu
    app_id: YOUR_APPID
    api_key: YOUR_APIKEY
    secret_key: YOUR_SECRETKEY
    person: 4
```

Configuration variables:

- **app_id** (*Required*): AppID for use this service, registered on Baidu.
- **api_key** (*Required*): Apikey from Baidu.
- **secret_key** (*Required*): Secretkey from Baidu.
- **speed** (*Optional*): Audio speed, from 0 to 9, default is 5.
- **pitch** (*Optional*): Audio pitch, from 0 to 9, default is 5.
- **volume** (*Optional*): Audio volume, from 0 to 15, default is 5.
- **person** (*Optional*): You can choose 0, 1, 3, 4, default is 0(a female voice).
