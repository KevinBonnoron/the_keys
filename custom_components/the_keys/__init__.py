"""The Keys integration."""
from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (CONF_PASSWORD, CONF_SCAN_INTERVAL,
                                 CONF_USERNAME, Platform)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from the_keyspy import TheKeysApi, TheKeysLock

from .const import CONF_GATEWAY_IP, DEFAULT_SCAN_INTERVAL, DOMAIN

PLATFORMS: list[Platform] = [Platform.LOCK, Platform.SENSOR]

_LOGGER = logging.getLogger(__name__)


async def async_setup_coordinator(hass: HomeAssistant, entry: ConfigEntry) -> DataUpdateCoordinator:
    """Set up the coordinator."""
    api = TheKeysApi(
        entry.data[CONF_USERNAME],
        entry.data[CONF_PASSWORD],
        entry.data[CONF_GATEWAY_IP] or None,
    )

    async def async_update_data():
        """Fetch data from API."""
        try:
            devices = await hass.async_add_executor_job(api.get_devices)
            for device in devices:
                if isinstance(device, TheKeysLock):
                    await hass.async_add_executor_job(device.retrieve_infos)

            return devices
        except Exception as e:
            _LOGGER.error("Error updating devices: %s", e)
            return None

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="the_keys",
        update_method=async_update_data,
        update_interval=timedelta(seconds=entry.data.get(
            CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)),
    )

    await coordinator.async_config_entry_first_refresh()
    return coordinator


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up The Keys from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    coordinator = await async_setup_coordinator(hass, entry)
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Handle removal of an entry."""
    if unloaded_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

        if not hass.data[DOMAIN]:
            hass.data.pop(DOMAIN)

    return unloaded_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
