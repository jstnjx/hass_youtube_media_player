import requests
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.entity_registry import async_get as async_get_entity_registry
from homeassistant.components.media_player import DOMAIN as MEDIA_PLAYER_DOMAIN

from .const import DOMAIN

class YouTubeMediaPlayerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle the config flow for YouTube Media Player."""

    async def async_step_user(self, user_input=None):
        """Handle the initial step of the config flow."""
        if user_input is not None:
            media_player_entity = user_input["media_player_entity"]
            youtube_api_key = user_input["youtube_api_key"]

            # Validate YouTube API Key
            if not await self._validate_youtube_api_key(youtube_api_key):
                return self.async_show_form(
                    step_id="user",
                    errors={"youtube_api_key": "invalid_api_key"},
                    data_schema=self._get_schema()
                )

            return self.async_create_entry(
                title=media_player_entity,
                data={
                    "media_player_entity": media_player_entity,
                    "youtube_api_key": youtube_api_key,
                },
            )

        return self.async_show_form(
            step_id="user",
            data_schema=self._get_schema(),
        )

    async def _validate_youtube_api_key(self, youtube_api_key: str) -> bool:
        """Validate the provided YouTube API key."""
        test_url = f"https://www.googleapis.com/youtube/v3/channels?part=snippet&key={youtube_api_key}"

        response = await self.hass.async_add_executor_job(requests.get, test_url)
        if response.status_code == 400:
            error = response.json().get("error", {}).get("message", "")
            if "API key not valid" in error:
                return False
        return True

    def _get_schema(self):
        """Generate the input schema."""
        media_players = self._get_media_players()
        return vol.Schema({
            vol.Required("media_player_entity"): vol.In(media_players),
            vol.Required("youtube_api_key"): cv.string,
        })

    def _get_media_players(self):
        """Get a list of all available media player entities."""
        registry = async_get_entity_registry(self.hass)
        return [
            entry.entity_id
            for entry in registry.entities.values()
            if entry.domain == MEDIA_PLAYER_DOMAIN
        ]
