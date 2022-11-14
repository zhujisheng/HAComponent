"""The environment_variables component."""

import logging
import os

import voluptuous as vol

from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.typing import ConfigType

DOMAIN = "environment_variables"

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema(
    {DOMAIN: {cv.string:cv.string}}, extra=vol.ALLOW_EXTRA
)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the environment_variables component."""
    conf = config.get(DOMAIN, {})

    for name in conf:
        os.environ[name] = conf.get(name)
        _LOGGER.warning("Set environment variable: %s=%s", name, conf.get(name))
    return True
