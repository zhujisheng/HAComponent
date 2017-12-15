聚合数据股票信息组件使用[聚合云API](https://www.juhe.cn/docs/api/id/21)。组件获得上海和深圳证交所的股票交易信息。

将以下内容放置在`configuration.yaml`文件中：
```yaml
# configuration.yaml样例
sensor:
  - platform: juhe_stock
    key: xxxxxxxxxxxxxxxxxxxx
    symbols:
      - sz000002
      - sh600600
      - sh600000
```
可配置项：
- **key** （*必选项*）: 聚合数据API的Key。
- **symbols** (*列表 可选项*): 股票代码列表. 如果未配置, 缺省值是sz000002 (万科A)。


### Description in English ###
The Juhe stock platform uses <a href="https://www.juhe.cn/docs/api/id/21" rel="noopener" target="_blank">Juhe's stock cloud api</a>. It can get the price of stock on Shanghai and Shenzhen's security market.

To enable a sensor with juhe_stock, add the following lines to your configuration.yaml:
```yaml
#Example configuration.yaml entry
sensor:
  - platform: juhe_stock
    key: xxxxxxxxxxxxxxxxxxxx
    symbols:
      - sz000002
      - sh600600
      - sh600000
```


variables:
<ul>
	<li><strong>key</strong>(<em>Required</em>): Key from Juhe.</li>
	<li><strong>symbols</strong> array(<em>Optional</em>): List of stock market symbols for given companies. If not specified, it defaults to sz000002 (万科A).</li>
</ul>

Put the file "juhe_stock.py" in the dir: "<code>~/.homeassistant/custom_components/sensor/</code>"
