"""The Keys Lock device."""
from homeassistant.components.lock import LockEntity
from homeassistant.components.sensor import (SensorDeviceClass, SensorEntity, SensorStateClass)
from the_keyspy import TheKeysLock

from .base import TheKeysEntity
from .const import DOMAIN


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up TheKeys lock devices."""
    devices = hass.data[DOMAIN]

    entities = []

    for device in devices:
        if isinstance(device, TheKeysLock):
            entities.append(TheKeysLockEntity(device))

    async_add_entities(entities, update_before_add=True)


class TheKeysLockEntity(TheKeysEntity, LockEntity):
    """TheKeys lock device implementation."""

    def __init__(self, device: TheKeysLock):
        super().__init__(device=device)

    def lock(self, **kwargs):
        """Lock the device."""
        self._device.close()
        self.async_write_ha_state()

    def unlock(self, **kwargs):
        """Unlock the device."""
        self._device.open()
        self.async_write_ha_state()

    def update(self) -> None:
        """Update the device."""
        self._device.retrieve_infos()

    @property
    def is_locked(self):
        """Return true if device is on."""
        return self._device.is_locked

    @property
    def type(self) -> str:
        return "lock"
