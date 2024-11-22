from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from .const import DOMAIN

async def async_setup_entry(hass: HomeAssistant, entry: config_entries.ConfigEntry):
    """Set up the YouTube Media Player from a config entry."""
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "media_player")
    )
    return True
