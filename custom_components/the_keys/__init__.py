"""The Keys integration."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import HomeAssistant
from the_keyspy import TheKeysApi

from .const import DOMAIN

PLATFORMS = ["lock", "sensor"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up The Keys from a config entry."""

    api = TheKeysApi(entry.data.get(CONF_USERNAME),
                     entry.data.get(CONF_PASSWORD))
    hass.data[DOMAIN] = await hass.async_add_executor_job(api.get_devices)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data.pop(DOMAIN)

    return unload_ok
