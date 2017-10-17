The Aliyun stock platform uses <a href="https://market.aliyun.com/products/57000002/cmapi017711.html" rel="noopener" target="_blank">Aliyun's stock cloud api</a>. It can get the price of stock on Shanghai and Shenzhen's security market.

To enable a sensor with aliyun_stock, add the following lines to your configuration.yaml:
<pre class="lang:yaml decode:true " >#Example configuration.yaml entry
sensor:
  - platform: aliyun_stock
    appcode: xxxxxxxxxxxxxxxxxxxx
    symbols:
      - sz000002
      - sh600600
      - sh600000
</pre> 


variables:
<ul>
	<li><strong>appcode</strong>(<em>Required</em>): AppCode from Aliyun.</li>
	<li><strong>symbols</strong> array(<em>Optional</em>): List of stock market symbols for given companies. If not specified, it defaults to sz000002 (万科A).</li>
</ul>

Put the file "aliyun_stock.py" in the dir: "<code>~/.homeassistant/custom_components/sensor/</code>"
