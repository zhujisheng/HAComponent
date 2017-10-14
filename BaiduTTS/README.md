The Baidu text-to-speech platform uses <a href="https://cloud.baidu.com/product/speech/tts">Baidu TTS engine</a> to read a text with natural sounding voices.

To enable text-to-speech with Baidu, add the following lines to your configuration.yaml:

<pre class="lang:yaml decode:true">
#Example configuration.yaml entry
tts:
  - platform: baidu
    appid: YOUR_APPID 
    apikey: YOUR_APIKEY
    secretkey: YOUR_SECRETKEY
    person: 4
</pre>
    
Configura</li>tion variables:
<ul><li>appid(Required): AppID for use this service, registered on Baidu.</li>
  <li>apikey(Required): Apikey from Baidu.</li>
<li>secretkey(Required): Secretkey from Baidu.</li>
<li>speed(Optional): Audio speed, from 0 to 9, default is 5.</li>
<li>pitch(Optional): Audio pitch, from 0 to 9, default is 5.</li>
<li>volume(Optional): Audio volume, from 0 to 15, default is 5.</li>
<li>person(Optional): You can choose 0, 1, 3, 4, default is 0(a female voice)</li>
</ul>

Put the file "baidu.py" in the dir: "~/.homeassistant/custom_components/tts/"
