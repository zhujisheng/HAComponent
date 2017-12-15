<h3>中文说明</h3>
聚合数据老黄历信息(juhe_laohuangli)从<a href="https://www.juhe.cn/docs/api/id/65" rel="noopener" target="_blank">聚合数据API</a>获得数据。
在HA的configuration.yaml中的配置：
<pre class="lang:yaml decode:true " >
#Example configuration.yaml entry
sensor:
  - platform: juhe_laohuangli
    key: xxxxxxxxxxxxxxxx
</pre>

配置变量：
<ul>
	<li>key(Required): 从聚合数据api申请获得的key.</li>
</ul>
将文件"juhe_laohuangli.py"放在以下目录: "<code>~/.homeassistant/custom_components/sensor/</code>"

<h3>Description in English</h3>
The Juhe Laohuangli uses Juhe's <a href="https://www.juhe.cn/docs/api/id/65" rel="noopener" target="_blank">Loahuangli api</a>.

To enable a sensor with juhe_laohuangli, add the following lines to your configuration.yaml:

<pre class="lang:yaml decode:true " >
#Example configuration.yaml entry
sensor:
  - platform: juhe_laohuangli
    key: xxxxxxxxxxxxxxxxxx
</pre>
variables:
<ul>
	<li>key(Required): Key from Juhe.</li>
</ul>
Put the file "juhe_laohuangli.py" in the dir: "<code>~/.homeassistant/custom_components/sensor/</code>"



