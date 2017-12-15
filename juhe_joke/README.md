<h3>中文说明</h3>
聚合笑话(juhe_joke)从<a href="https://www.juhe.cn/docs/api/id/95/aid/281">聚合数据API</a>获得数据。
在HA的configuration.yaml中的配置：
<pre class="lang:yaml decode:true " >
#Example configuration.yaml entry
sensor:
  - platform: juhe_joke
    key: xxxxxxxxxxxxxxxx
</pre>

配置变量：
<ul>
	<li>key(Required): 从聚合数据api申请获得的key.</li>
</ul>
将文件"juhe_joke.py"放在以下目录: "<code>~/.homeassistant/custom_components/sensor/</code>"。
每天会更新20条笑话信息。如果您想更换，调用服务“sensor.jokes_update”。

<h3>description in English</h3>
The Joke sensor uses Juhe's <a href="https://www.juhe.cn/docs/api/id/95/aid/281">open platform's joke api</a>.

To enable a sensor with juhe_joke, add the following lines to your configuration.yaml:
<pre class="lang:yaml decode:true " >
#Example configuration.yaml entry
sensor:
  - platform: juhe_joke
    key: xxxxxxxxxxxxxxxxxx
</pre>
variables:
<ul>
	<li>key(Required): Key from Juhe.</li>
</ul>
Put the file "juhe_joke.py" in the dir: "<code>~/.homeassistant/custom_components/sensor/</code>"
The sensor update imformation every day(get 20 jokes from Juhe), if you want to change some jokes, call service "sensor.jokes_update".
