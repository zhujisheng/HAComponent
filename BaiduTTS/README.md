The Baidu text-to-speech platform uses Baidu TTS engine to read a text with natural sounding voices.

To enable text-to-speech with Baidu, add the following lines to your configuration.yaml:

<pre><code>
#Example configuration.yaml entry
tts:
  - platform: baidu
    appid: YOUR_APPID 
    apikey: YOUR_APIKEY
    secretkey: YOUR_SECRETKEY
</code></pre>
    
Configuration variables:
*appid(Required): AppID for use this service, registered on Baidu.
*apikey(Required): Apikey from Baidu.
*secretkey(Required): Secretkey from Baidu.
*speed(Optional): Audio speed, from 0 to 9, default is 5.
*pitch(Optional): Audio pitch, from 0 to 9, default is 5.
*volume(Optional): Audio volume, from 0 to 15, default is 5.
*person(Optional): You can choose 0, 1, 3, 4, default is 0(a female voice)

