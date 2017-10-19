service based on http://lbs.amap.com/api/webservice/guide/api/direction/

<pre class="lang:yaml decode:true">
sensor:
  - platform: gaode_travel_time
    api_key: XXXXXXXXXXXXXXXXXXXXXXXX
    name: nameofentity   #optional, only support english
    friendly_name: 从家去公司  #optional, for display, can be Chinese
    travel_mode: driving     #optional, support driving and walking, default is driving
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

Put the file "gaode_travel_time.py" in the dir: "~/.homeassistant/custom_components/sensor/"
