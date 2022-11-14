*本组件设置homeassistant运行时的环境变量*

## 配置


```yaml
# configuration.yaml
environment_variables:
  HTTPS_PROXY: http://homeassistant:7088
```

以上配置设置HTTPS_PROXY环境变量。

比如，如果您在墙内想要直接使用官方的google_translate_tts集成，可以安装[simple-proxy Add-on](https://github.com/zhujisheng/hassio-addons/tree/master/simple-proxy)，然后按照以上配置即可。
