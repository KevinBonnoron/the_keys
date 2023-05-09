"""The Keys Lock device."""
from homeassistant.components.lock import LockEntity
from the_keyspy import TheKeysLock

from .base import TheKeysEntity
from .const import DOMAIN


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up TheKeys lock devices."""
    the_keys_api = hass.data[DOMAIN]

    entities = []

    for device in await hass.async_add_executor_job(the_keys_api.get_devices):
        if isinstance(device, TheKeysLock):
            entities.append(TheKeysLockEntity(device))

    async_add_entities(entities)


class TheKeysLockEntity(TheKeysEntity, LockEntity):
    """TheKeys lock device implementation."""

    def lock(self, **kwargs):
        """Lock the device."""
        self._attr_is_locking = True
        self._device.lock()
        self._attr_is_locking = False

    def unlock(self, **kwargs):
        """Unlock the device."""
        self._attr_is_unlocking = True
        self._device.unlock()
        self._attr_is_unlocking = False

    def update(self) -> None:
        """Update the device."""
        self._device.retrieve_infos()

    @property
    def is_locked(self):
        """Return true if device is on."""
        return self._device.is_locked
