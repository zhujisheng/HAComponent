"""

For more details about HAChina,
https://www.hachina.io/
"""
import asyncio
import logging
import json
import subprocess
import shutil
import re
import os

from aiohttp import web

import voluptuous as vol
from homeassistant.components.http import HomeAssistantView
from homeassistant.components.http import setup_cors

#from . import redpoint_agent as rpa

DOMAIN = 'redpoint'
URL = '/' + DOMAIN


_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({}),
}, extra=vol.ALLOW_EXTRA)

class redpoint_agent(object):


    def __init__(self):
        self.VERSION = "0.0.2"
        self.config = {}
        self.startupinfo = None
        if os.name == 'nt':
            self.startupinfo = subprocess.STARTUPINFO()
            self.startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    def detectConfigPath(self):
        data_dir = os.getenv('APPDATA') if os.name == "nt" \
            else os.path.expanduser('~')
        return os.path.join(data_dir, '.homeassistant')


    def editingConfigPath(self):
        data_dir = os.getenv('APPDATA') if os.name == "nt" \
            else os.path.expanduser('~')
        return os.path.join(data_dir, '.haconfig_tmp')


    def ignored_files(self,adir, filenames):
        return [filename for filename in filenames if
                filename == "deps"
                or filename.endswith('.db')
                ]


    def copyConfig(self, src):
        to = self.config["editing_config_path"]
        if os.path.exists(to):
            shutil.rmtree(to)
        shutil.copytree(src, to, ignore=self.ignored_files)

rpa = redpoint_agent()

@asyncio.coroutine
def setup(hass, config=None):
    """Set up the component."""
    rpa.config['config_path'] = rpa.detectConfigPath()
    rpa.config["editing_config_path"] = rpa.editingConfigPath()
    rpa.copyConfig(rpa.config['config_path'])
    
    hass.http.register_view(RedpointCheckView)
    hass.http.register_view(RedpointConfigurationView)
    hass.http.register_view(RedpointInfoView)
    hass.http.register_view(RedpointView)

    #setup_cors(hass.http.app, ["http://configurator.hachina.io"])

    yield from hass.components.frontend.async_register_built_in_panel(
        'iframe', "红点", "mdi:hand-pointing-right",
            'redpoint_config', {'url': URL})
    return True


class RedpointCheckView(HomeAssistantView):
    """View to return defined themes."""

    requires_auth = True
    url = "/redpoint/check"
    name = "Redpoint:check"

    @asyncio.coroutine
    def get(self, request):
        """Return themes."""
        cmd = ["hass", "--script", "check_config",
               "-c", rpa.config['editing_config_path']]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             stdin=subprocess.PIPE,
                             startupinfo=rpa.startupinfo)
        out, err = p.communicate()
        if(err):
            raise Exception(err)

        if os.name == "nt":
            out = out.decode('gb2312')
        else:
            out = out.decode()

        return web.Response(text=out, content_type="text/html")


class RedpointConfigurationView(HomeAssistantView):
    """View to return defined themes."""

    requires_auth = True
    url = "/redpoint/configuration"
    name = "Redpoint:configuration"


    @asyncio.coroutine
    def get(self, request):
        """Return themes."""
        path = rpa.config['editing_config_path'] + '/configuration.yaml'
        with open(path, 'r', encoding='utf8') as configuration:
            content = configuration.read()

        return web.Response(text=content, content_type="text/html")

    @asyncio.coroutine
    def post(self, request):
        """Return themes."""
        path = rpa.config['editing_config_path'] + '/configuration.yaml'
        with open(path, 'w', encoding='utf8') as configuration:
            configuration.write(request.get_json()['data'])

        return web.Response(text='', content_type="text/html")



class RedpointInfoView(HomeAssistantView):
    """View to return defined themes."""

    requires_auth = True
    url = "/redpoint/info"
    name = "Redpoint:info"

    @asyncio.coroutine
    def get(self, request):
        """Return themes."""

        msg = json.dumps(rpa.config)

        return web.Response(text=msg, content_type="text/html")



class RedpointView(HomeAssistantView):
    """View to return defined themes."""

    requires_auth = True
    url = URL
    name = DOMAIN

    @asyncio.coroutine
    def get(self, request):
        """Return themes."""

        #msg = "<script>window.location.assign(\"http://\"+location.hostname+\":5000\");</script>"
        msg = "<script>window.location.assign(\"http://configurator.hachina.io/config?agent=" + str(request.url.origin()) + "\");</script>"

        return web.Response(text=msg, content_type="text/html")





        
