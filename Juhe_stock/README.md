The Juhe stock platform uses <a href="https://www.juhe.cn/docs/api/id/21" rel="noopener" target="_blank">Juhe's stock cloud api</a>. It can get the price of stock on Shanghai and Shenzhen's security market.

To enable a sensor with aliyun_stock, add the following lines to your configuration.yaml:
<pre class="lang:yaml decode:true " >#Example configuration.yaml entry
sensor:
  - platform: Juhe_stock
    key: xxxxxxxxxxxxxxxxxxxx
    symbols:
      - sz000002
      - sh600600
      - sh600000
</pre> 


variables:
<ul>
	<li><strong>key</strong>(<em>Required</em>): Key from Juhe.</li>
	<li><strong>symbols</strong> array(<em>Optional</em>): List of stock market symbols for given companies. If not specified, it defaults to sz000002 (万科A).</li>
</ul>

Put the file "juhe_stock.py" in the dir: "<code>~/.homeassistant/custom_components/sensor/</code>"
