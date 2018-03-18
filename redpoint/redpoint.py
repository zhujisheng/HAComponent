"""

For more details about HAChina,
https://www.hachina.io/
"""
#import asyncio
import subprocess
import shutil
import os
import time

class redpoint_agent(object):

    def __init__(self, ConfigPath=None, EditPath=None, Cmd_hass='hass'):
        self._version = '0.0.3'

        if os.name == 'nt':
            self._startupinfo = subprocess.STARTUPINFO()
            self._startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        else:
            self._startupinfo = None

        self._config = {}
        if ConfigPath is None:
            self._config['config_path']=self._detectConfigPath()
        else:
            self._config['config_path']=ConfigPath

        if EditPath is None:
            self._config['editing_config_path']=self._editingConfigPath()
        else:
            self._config['editing_config_path']=EditPath

        self._Cmd_hass = Cmd_hass


    def _detectConfigPath(self):
        data_dir = os.getenv('APPDATA') if os.name == 'nt' \
            else os.path.expanduser('~')
        return os.path.join(data_dir, '.homeassistant')


    def _editingConfigPath(self):
        data_dir = os.getenv('APPDATA') if os.name == 'nt' \
            else os.path.expanduser('~')
        return os.path.join(data_dir, '.haconfig_tmp')


    def _ignored_files(self,adir, filenames):
        return [filename for filename in filenames if
                (adir.endswith('deps') and filename=='man')
                or (('deps' in adir) and ('Python' in adir) and filename=='Scripts')
                or (adir.endswith('site-packages') and ('colorlog' not in filename))
                or filename == 'tts'
                or filename.endswith('.db')
                #or filename == '__pycache__'
                ]

    def copyConfig(self):
        to = self._config['editing_config_path']
        if os.path.exists(to):
            shutil.rmtree(to)
        shutil.copytree(self._config['config_path'], to, ignore=self._ignored_files)

    def Check(self):
        cmd = [self._Cmd_hass, "--script", "check_config",
               "-c", self._config['editing_config_path']]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             stdin=subprocess.PIPE,
                             startupinfo=self._startupinfo)
        out, err = p.communicate()
        #p = yield from asyncio.create_subprocess_exec(*cmd,
        #                                              stdout=asyncio.subprocess.PIPE,
        #                                              stderr=asyncio.subprocess.PIPE,
        #                                              stdin=asyncio.subprocess.PIPE,
        #                                              )
        #out, err = yield from p.communicate()
        if(err):
            raise Exception(err)

        if os.name == "nt":
            out = out.decode('gb2312')
        else:
            out = out.decode()

        return out

    def ReadConfiguration(self):
        path = os.path.join(self._config['editing_config_path'], 'configuration.yaml')
        with open(path, 'r', encoding='utf8') as configuration:
            content = configuration.read()

        return content

    def WriteConfiguration(self, content):
        path = os.path.join(self._config['editing_config_path'], 'configuration.yaml')
        with open(path, 'w', encoding='utf8') as configuration:
            configuration.write(content)

        return True

    def Publish(self):
        file_from = os.path.join(self._config['editing_config_path'] , 'configuration.yaml')
        file_to = os.path.join(self._config['config_path'] , 'configuration.yaml')
        file_backup = file_to + '.' + time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
        shutil.copyfile(file_to, file_backup)
        shutil.copyfile(file_from, file_to)
        return True


    @property
    def config(self):
        return self._config

    @property
    def version(self):
        return self._version


import logging
import asyncio
from aiohttp import web
import json
import uuid

import voluptuous as vol
from homeassistant.util.async import run_coroutine_threadsafe
from homeassistant.components.http import HomeAssistantView
from homeassistant.components.http import setup_cors

#from .redpoint_agent import redpoint_agent

DOMAIN = 'redpoint'

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({}),
}, extra=vol.ALLOW_EXTRA)


#@asyncio.coroutine
def setup(hass, config=None):
    """Set up the component."""

    rpa = redpoint_agent(ConfigPath=hass.config.config_dir)
    rpa.copyConfig()

    token = '/%s'%(str(uuid.uuid4()))

    views={
        "Redpoint:root":["/redpoint", True, RedpointRootView],
        "Redpoint:redirect":["%s/redpoint/redirect"%(token), False, RedpointRedirectView],
        "Redpoint:check":["%s/redpoint/check"%(token), False, RedpointCheckView],
        "Redpoint:configuration":["%s/redpoint/configuration"%(token), False, RedpointConfigurationView],
        "Redpoint:info":["%s/redpoint/info"%(token), False, RedpointInfoView],
        "Redpoint:version":["%s/redpoint/version"%(token), False, RedpointVersionView],
        "Redpoint:publish":["%s/redpoint/publish"%(token), False, RedpointPublishView],
        }
    for name, t in views.items():
        view = t[2]()
        setattr( view, 'name', name )
        setattr( view, 'url', t[0] )
        setattr( view, 'requires_auth', t[1] )
        setattr( view, 'rpa', rpa )
        setattr( view, 'token', token )
        setattr( view, 'hass', hass )

        hass.http.register_view(view)

    if not "cors_allowed_origins" in config["http"]:
        setup_cors(hass.http.app, ["http://configurator.hachina.io"])

    #yield from hass.components.frontend.async_register_built_in_panel(
    #    'iframe', "红点", "mdi:hand-pointing-right",
    #    'redpoint_config', {'url': views["Redpoint:redirect"][0]})
    run_coroutine_threadsafe(hass.components.frontend.async_register_built_in_panel(
                           'iframe', "红点", "mdi:hand-pointing-right",
                           'redpoint_config', {'url': views["Redpoint:redirect"][0]}),
                             hass.loop
                       )
    return True

class RedpointRootView(HomeAssistantView):
    """View to return defined themes."""
    @asyncio.coroutine
    def get(self, request):
        """Return themes."""
        msg = "<script>window.location.assign(\"http://configurator.hachina.io/config?agent=%s%s\");</script>"%(str(request.url.origin()), self.token)
        return web.Response(text=msg, content_type="text/html")

class RedpointRedirectView(HomeAssistantView):
    """View to return defined themes."""
    @asyncio.coroutine
    def get(self, request):
        """Return themes."""
        msg = "<script>window.location.assign(\"http://configurator.hachina.io/config?agent=%s%s\");</script>"%(str(request.url.origin()), self.token)
        return web.Response(text=msg, content_type="text/html")


class RedpointCheckView(HomeAssistantView):
    """View to return defined themes."""
    @asyncio.coroutine
    def get(self, request):
        """Return themes."""
        #out = self.rpa.Check()
        out = yield from self.hass.async_add_job(self.rpa.Check)
        return web.Response(text=out, content_type="text/html")


class RedpointConfigurationView(HomeAssistantView):
    """View to return defined themes."""
    @asyncio.coroutine
    def get(self, request):
        """Return themes."""
        out = yield from self.hass.async_add_job(self.rpa.ReadConfiguration)
        return web.Response(text=out, content_type="text/html")

    @asyncio.coroutine
    def post(self, request):
        """Return themes."""
        content= yield from request.json()

        result = yield from self.hass.async_add_job(self.rpa.WriteConfiguration, content['data'])
        if result:
            out = 'OK'
        else:
            out = 'KO'
        return web.Response(text=out, content_type="text/html")


class RedpointInfoView(HomeAssistantView):
    """View to return defined themes."""
    @asyncio.coroutine
    def get(self, request):
        """Return themes."""
        out = json.dumps(self.rpa.config)
        return web.Response(text=out, content_type="text/html")

class RedpointVersionView(HomeAssistantView):
    """View to return defined themes."""
    @asyncio.coroutine
    def get(self, request):
        """Return themes."""
        out = self.rpa.version
        return web.Response(text=out, content_type="text/html")


class RedpointPublishView(HomeAssistantView):
    """View to return defined themes."""
    @asyncio.coroutine
    def get(self, request):
        """Return themes."""
        result = yield from self.hass.async_add_job(self.rpa.Publish)
        if result:
            out = 'OK'
        else:
            out = 'KO'
        return web.Response(text=out, content_type="text/html")
