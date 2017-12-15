<h3>中文说明</h3>
高德地图行程时间（gaode_travel_time）使用高德的API获得信息：http://lbs.amap.com/api/webservice/guide/api/direction/.

如下配置configuration.yaml文件：
<pre class="lang:yaml decode:true">
sensor:
  - platform: gaode_travel_time
    api_key: XXXXXXXXXXXXXXXXXXXXXXXX
    name: driving_working
    friendly_name: 从家去公司
    travel_mode: driving
    strategy: 0       #optional, 0-9, default 0 速度最快
    origin:
      #longitude_latitude: 116.481028,39.989643
      city: 上海
      address: 凤城路
    destination:
      #longitude_latitude: 121.3997,31.0456
      city: 上海
      address: 广富林路
</pre>
变量说明:
<ul>
	<li>api_key(Required): 从高德开放平台申请获得的APIKEY。</li>
  <li>name(Optional): 实体的名称，不能是中文，缺省值是gaode_travel_time。</li>
  <li>friendly_name(Optional): 在界面上显示的名称，可以是中文。</li>
  <li>travel_mode(Optional): 行程模式，可以是driving、walking或bicycling，缺省为driving。</li>
  <li>strategy(Optional): 当travel_mode是driving时有效，支持0-9, 缺省为0（代表选择最快路径）。其余的选项可以参加高德开放平台上的描述。</li>
  <li>origin(Required): 行程开始点。可以配置为longitude_latitude或者(city, address)。</li>
  <li>destination(Required): 行程结束点。可以配置为longitude_latitude或者(city, address)。</li>
  <li>longitude_latitude(Optional): 维度和经度信息，维度在前，经度在后，用逗号隔开。</li>
  <li>city(Optional): 城市名</li>
  <li>address(Optional): 具体的地址描述</li>
</ul>
将文件"gaode_travel_time.py"放置在以下目录: "~/.homeassistant/custom_components/sensor/"。

组件每半小时更新一次信息，如果想获得当前的信息，调用服务："sensor.gaode_travel_time_update"。


<h3>Description in English</h3>
The gaode_travel_time sensor uses Gaode open api http://lbs.amap.com/api/webservice/guide/api/direction/.

To enable a sensor with gaode_travel_time, add the following lines to your configuration.yaml:

<pre class="lang:yaml decode:true">
sensor:
  - platform: gaode_travel_time
    api_key: XXXXXXXXXXXXXXXXXXXXXXXX
    friendly_name: 从家去公司
    travel_mode: driving
    strategy: 0       #optional, 0-9, default 0 速度最快
    origin:
      #longitude_latitude: 116.481028,39.989643
      city: 上海
      address: 凤城路
    destination:
      #longitude_latitude: 121.3997,31.0456
      city: 上海
      address: 广富林路
</pre>
variables:
<ul>
	<li>api_key(Required): Key from Gaode.</li>
  <li>name(Optional): Entity's ObjectID，the default is gaode_travel_time。</li>
  <li>friendly_name(Optional): sensor's display name, can be Chinese</li>
  <li>travel_mode(Optional): travel mode, support driving, walking and bicycling, default is driving</li>
  <li>strategy(Optional): Used when the travel_mode is driving, support 0-9, default is 0, means choose the fast route. </li>
  <li>origin(Required): The start address. You can configure with longitude_latitude or (city, address) imformation.</li>
  <li>destination(Required): The destination address. You can configure with longitude_latitude or (city, address) imformation.</li>
  <li>longitude_latitude(Optional): The longitude and latitudu of the address</li>
  <li>city(Optional): The Chinese city name</li>
  <li>address(Optional): The address in Chinese</li>
</ul>
Put the file "gaode_travel_time.py" in the dir: "~/.homeassistant/custom_components/sensor/"

The sensor update imformation every half hour, if you want the current imformation, can call service "sensor.gaode_travel_time_update".
