"""Config flow for Pulse Audio integration."""
import logging
import asyncio
import shlex
import voluptuous as vol
from subprocess import PIPE, Popen

from homeassistant import config_entries, core, exceptions
from homeassistant.const import CONF_NAME

from .const import DOMAIN, CONF_SINK   # pylint:disable=unused-import

_LOGGER = logging.getLogger(__name__)

async def get_sinks():
    cmd = "pactl list short sinks"
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)
    stdout, _ = await proc.communicate()
    return  {shlex.split(d)[1]:shlex.split(d)[0]+":"+shlex.split(d)[1] for d in stdout.decode().splitlines()}

async def validate_input(hass: core.HomeAssistant, data):
    """Validate the user input allows us to connect.

    Data has the keys from DATA_SCHEMA with values provided by the user.
    """

    sinks = await get_sinks()

    if data[CONF_SINK] not in sinks:
        raise InvalidSinkID

    # Return info that you want to store in the config entry.
    return {"title": "PulseAudio: "+data[CONF_SINK]}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Pulse Audio."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)

                return self.async_create_entry(title=info["title"], data=user_input)
            except InvalidSinkID:
                errors["base"] = "invalid_sink_id"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        sinks = await get_sinks()
        #sinks = {sink.id:sink.name+':'+sink.id for sink in all_speakers()}
        DATA_SCHEMA = vol.Schema(
            {vol.Required(CONF_NAME, default="PulseAudio Speaker"): str,
            vol.Required(CONF_SINK): vol.In(sinks)}
            )
        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )

class InvalidSinkID(exceptions.HomeAssistantError):
    """Error to indicate there is invalid sink ID."""
