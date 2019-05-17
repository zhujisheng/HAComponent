"""

For more details about HAChina,
https://www.hachina.io/
"""
import asyncio
import logging
import os
import uuid
import base64
import hashlib

import voluptuous as vol
from homeassistant.core import Event
from homeassistant.helpers import config_validation as cv
from homeassistant.components.weblink import Link
from homeassistant.const import EVENT_HOMEASSISTANT_STOP
from homeassistant.helpers.event import async_call_later


DOMAIN = 'tunnel2local'
DATA_TUNNEL2LOCAL = 'tunnel2local'


CONF_FRPS = "frps"
CONF_FRPS_PORT = "frps_port"
CONF_FRPC_BIN = "frpc_bin"
CONF_TOKEN = "frp_token"
CONF_REMOTE_PORT = "remote_port"
CONF_SUBDOMAIN = "subdomain"

DEFAULT_FRPS_PORT = 7000
DEFAULT_FRPC_BIN = "frpc"
DEFAULT_TOKEN = ""
DEFAULT_REMOTE_PORT = 8123

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Optional(CONF_FRPS): cv.string,
                vol.Optional(CONF_FRPS_PORT, default=DEFAULT_FRPS_PORT): cv.port,
                vol.Optional(CONF_FRPC_BIN, default=DEFAULT_FRPC_BIN): cv.string,
                vol.Optional(CONF_TOKEN, default=DEFAULT_TOKEN): cv.string,
                vol.Optional(CONF_REMOTE_PORT, default=DEFAULT_REMOTE_PORT): cv.port,
                vol.Optional(CONF_SUBDOMAIN): cv.string,
            }),
    },
    extra=vol.ALLOW_EXTRA)


@asyncio.coroutine
def async_setup(hass, config):
    """Set up the component."""
    conf = config[DOMAIN]
    
    port_local = hass.config.api.port
    command = conf.get(CONF_FRPC_BIN)

    subdomain = conf.get(CONF_SUBDOMAIN)
    if subdomain is None:
        mid1 = uuid.getnode()
        mid2 = mid1.to_bytes((mid1.bit_length() + 7) // 8, byteorder='big')
        mid3 = base64.b32encode(mid2)
        subdomain = mid3.decode().rstrip('=').lower()

    if conf.get(CONF_FRPS) is None:
        host = "ec2-18-221-17-124.us-east-2.compute.amazonaws.com"
        port = 7000
        token = "welcome2ha"
        subdomain_host = "hachina.802154.com"

        h = hashlib.md5()
        h.update(bytes(token,encoding='utf-8'))
        h.update(b'\xe4\xb3\xad\xe1\x96\x37')
        h.update(bytes("hachina",encoding='utf-8'))
        token = h.hexdigest()

        url = "http://%s.%s"%(subdomain, subdomain_host)
        
        run_cmd = [command,
                   'http',
                   '-s', "%s:%d"%(host,port),
                   '--sd', subdomain,
                   '-d', subdomain,
                   '-i', get_local_ip(),
                   '-l', str(port_local),
                   '-t', token,
                   '-n', 'hachina_'+subdomain,
                   '--locations', '/',
                   '--http_user', '',
                   '--http_pwd', '',
                   ]

    else:
        host = conf.get(CONF_FRPS)
        port = conf.get(CONF_FRPS_PORT)
        token = conf.get(CONF_TOKEN)
        remote_port = conf.get(CONF_REMOTE_PORT)
        url = "http://%s:%d"%(host, remote_port)

        run_cmd = [command,
                   'tcp',
                   '-s', "%s:%d"%(host,port),
                   '-i', get_local_ip(),
                   '-l', str(port_local),
                   '-t', token,
                   '-r', str(remote_port),
                   '-n', 'hachina_'+subdomain,
                   ]

    try:
        process = yield from run2(run_cmd)
    except:
        _LOGGER.error("Can't start %s", run_cmd[0])
        return False

    hass.data[DATA_TUNNEL2LOCAL] = process

    _LOGGER.info("tunnel2local started, hass can be visited from internet - %s", url)

    Link(hass, "Internet Address", url, "mdi:router-wireless")

    def probe_frpc(now):
        if(process.returncode):
            _LOGGER.error("frpc exited, returncode: %d", process.returncode )
        else:
            _LOGGER.info("frpc pid: %d", process.pid )

    async_call_later(hass, 60, probe_frpc)

    def stop_frpc(event: Event):
        """Stop frpc process."""
        hass.data[DATA_TUNNEL2LOCAL].terminate()

    hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, stop_frpc)

    return True

# Taken from: http://stackoverflow.com/a/11735897
def get_local_ip():
    import socket
    """Try to determine the local IP address of the machine."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Use Google Public DNS server to determine own IP
        sock.connect(('8.8.8.8', 80))

        return sock.getsockname()[0]
    except socket.error:
        try:
            return socket.gethostbyname(socket.gethostname())
        except socket.gaierror:
            return '127.0.0.1'
    finally:
        sock.close()


@asyncio.coroutine
def run2(frpc_command):
    #_LOGGER.error(frpc_command)

    p = yield from asyncio.create_subprocess_exec(*frpc_command, stdout=asyncio.subprocess.PIPE,
                         stderr=asyncio.subprocess.PIPE,
                         stdin=asyncio.subprocess.PIPE)
    return p

