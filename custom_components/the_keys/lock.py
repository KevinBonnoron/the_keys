"""The Keys Lock device."""
import logging

from homeassistant.components.lock import LockEntity
from the_keyspy import TheKeysLock

from .base import TheKeysEntity
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up TheKeys lock devices."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    if not coordinator.data:
        return

    entities = []
    for device in coordinator.data:
        if isinstance(device, TheKeysLock):
            entities.append(TheKeysLockEntity(coordinator, device))

    async_add_entities(entities)


class TheKeysLockEntity(TheKeysEntity, LockEntity):
    """TheKeys lock device implementation."""

    def __init__(self, coordinator, device: TheKeysLock):
        """Init a TheKeys lock entity."""
        super().__init__(coordinator, device=device)
        self._attr_unique_id = f"{self._device.id}_lock"

    @property
    def is_locked(self) -> bool:
        """Return whether the lock is locked."""
        return self._device.is_locked

    def lock(self, **kwargs):
        """Lock the device."""
        self._device.close()

    def unlock(self, **kwargs):
        """Unlock the device."""
        self._device.open()
