"""
Support for PulseAudio speakers(sinks)

"""
from __future__ import annotations
import voluptuous as vol
import logging
import asyncio

from homeassistant.components.media_player.const import (
    MEDIA_TYPE_MUSIC,
    SUPPORT_BROWSE_MEDIA,
    SUPPORT_PLAY,
    SUPPORT_PLAY_MEDIA,
    SUPPORT_VOLUME_SET,
)

from homeassistant.components.media_player import (
    BrowseMedia,
    async_process_play_media_url,
    MediaPlayerEntity,
    PLATFORM_SCHEMA)
from homeassistant.const import (
    CONF_NAME, STATE_IDLE, STATE_PLAYING)
import homeassistant.helpers.config_validation as cv
from homeassistant.components.ffmpeg import DATA_FFMPEG
from homeassistant.components import media_source

from .ffmpeg2pa import AudioPlay

from .const import (
    DOMAIN,
    CONF_SINK,
    DEFAULT_NAME,
    DEFAULT_SINK,
)

SUPPORT_PULSEAUDIO = (
    SUPPORT_PLAY
    | SUPPORT_PLAY_MEDIA
    | SUPPORT_VOLUME_SET
    | SUPPORT_BROWSE_MEDIA
)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Optional(CONF_SINK, default=DEFAULT_SINK): cv.string,
})

_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Setup the Pulse Audio Speaker platform."""
    name = config.get(CONF_NAME)
    sink = config.get(CONF_SINK)

    async_add_entities([PulseAudioSpeaker(hass, name, sink)])
    return True


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Add Pulse Audio entities from a config_entry."""
    name = config_entry.data[CONF_NAME]
    sink = config_entry.data[CONF_SINK]

    async_add_entities([PulseAudioSpeaker(hass, name, sink)])


class PulseAudioSpeaker(MediaPlayerEntity):
    """Representation of a Pulse Audio Speaker local."""

    def __init__(self, hass, name, sink):
        """Initialize the device."""

        self._hass = hass
        self._name = name
        self._sink = sink
        self._state = STATE_IDLE
        self._volume = 1.0
        if(sink == DEFAULT_SINK):
            device_option = ""
        else:
            device_option = "--device=%s"%(sink)
        self._AudioPlayer = AudioPlay(hass.data[DATA_FFMPEG].binary, device_option)

    @property
    def name(self):
        """Return the name of the device."""
        return self._name

    @property
    def unique_id(self):
        """Return the unique ID of the device."""
        return self._sink

    @property
    def state(self):
        """Return the state of the device."""
        return self._state

    @property
    def volume_level(self):
        """Volume level of the media player (0..1)."""
        return self._volume

    @property
    def supported_features(self):
        """Flag media player features that are supported."""
        return SUPPORT_PULSEAUDIO

    def play_media(self, media_type, media_id, **kwargs):
        """Send play commmand."""

        if media_source.is_media_source_id(media_id):
            sourced_media = asyncio.run_coroutine_threadsafe(
                                media_source.async_resolve_media(self._hass, media_id),
                                self._hass.loop
                                ).result()
            media_type = sourced_media.mime_type
            media_id = sourced_media.url

        if media_type != MEDIA_TYPE_MUSIC and not media_type.startswith("audio/"):
            raise HomeAssistantError(
                f"Invalid media type {media_type}. Only {MEDIA_TYPE_MUSIC} is supported"
            )

        # If media ID is a relative URL, we serve it from HA.
        media_id = async_process_play_media_url(
            self._hass, media_id
        )

        _LOGGER.info('play_media: %s', media_id)
        self._AudioPlayer.play(media_id)
        self._state = STATE_PLAYING
        self.schedule_update_ha_state()

    def set_volume_level(self, volume):
        """Set volume level, range 0..1."""
        self._AudioPlayer.set_volume(int(volume * 65536))
        self._volume = volume
        self.schedule_update_ha_state()

    def media_stop(self):
        """Send stop command."""
        self._AudioPlayer.stop()
        self._state = STATE_IDLE
        self.schedule_update_ha_state()

    def update(self):
        """Get the latest details from the device."""
        if self._AudioPlayer.is_running:
            self._state = STATE_PLAYING
        else:
            self._state = STATE_IDLE
        self._volume = self._AudioPlayer.volume/65536.0
        return True

    async def async_browse_media(
        self, media_content_type: str | None = None, media_content_id: str | None = None
    ) -> BrowseMedia:
        """Implement the websocket media browsing helper."""
        return await media_source.async_browse_media(
            self.hass,
            media_content_id,
            content_filter=lambda item: item.media_content_type.startswith("audio/"),
        )