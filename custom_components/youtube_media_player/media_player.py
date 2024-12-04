import logging
import requests
from homeassistant.components.media_player import MediaPlayerEntity
from homeassistant.components.media_player.const import MediaPlayerState
from homeassistant.helpers.update_coordinator import CoordinatorEntity

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the YouTube Media Player entity from a config entry."""
    media_player_entity = config_entry.data["media_player_entity"]
    youtube_api_key = config_entry.data["youtube_api_key"]

    async_add_entities([YouTubeMediaPlayer(hass, media_player_entity, youtube_api_key)])


class YouTubeMediaPlayer(MediaPlayerEntity):
    """Representation of the YouTube Media Player entity."""

    def __init__(self, hass, media_player_entity, youtube_api_key):
        """Initialize the YouTube Media Player."""
        self.hass = hass
        self._media_player_entity = media_player_entity
        self._youtube_api_key = youtube_api_key
        self._state = MediaPlayerState.IDLE
        self._media_title = None
        self._media_artist = None
        self._entity_picture = None

    @property
    def name(self):
        """Return the name of the entity."""
        return f"YouTube Media Player ({self._media_player_entity})"

    @property
    def state(self):
        """Return the current state."""
        return self._state

    @property
    def media_title(self):
        """Return the current media title."""
        return self._media_title

    @property
    def media_artist(self):
        """Return the current media artist."""
        return self._media_artist

    @property
    def entity_picture(self):
        """Return the URL of the entity picture."""
        return self._entity_picture

    async def async_update(self):
        """Update the entity state and attributes."""
        state = self.hass.states.get(self._media_player_entity)

        if state is not None:
            new_state = state.state
            media_title = state.attributes.get("media_title")
            media_artist = state.attributes.get("media_artist")
            source = state.attributes.get("source")

            # Check if the source is YouTube
            if source == "YouTube":
                if (
                    new_state != self._state
                    or media_title != self._media_title
                    or media_artist != self._media_artist
                ):
                    self._state = new_state
                    self._media_title = media_title
                    self._media_artist = media_artist
                    self._entity_picture = await self._get_youtube_thumbnail(
                        media_title, media_artist
                    )
            else:
                # If the source is not YouTube, set state to idle
                self._state = MediaPlayerState.IDLE
                self._media_title = None
                self._media_artist = None
                self._entity_picture = None

    async def _get_youtube_thumbnail(self, media_title, media_artist):
        """Fetch the YouTube thumbnail for the given title and artist."""
        if not media_title or not media_artist:
            return None

        search_url = (
            f"https://www.googleapis.com/youtube/v3/search?key={self._youtube_api_key}"
            f"&q={media_title} {media_artist}&type=video&maxResults=1&part=snippet"
        )

        response = await self.hass.async_add_executor_job(requests.get, search_url)

        if response.status_code == 200:
            data = response.json()
            if data.get("items"):
                return data["items"][0]["snippet"]["thumbnails"]["high"]["url"]

        elif response.status_code == 403:
            self._media_title = "Error 403"
            self._media_artist = "API KEY RATE LIMIT REACHED"
            return None

        return None
