"""The Keys Lock device."""
import logging

from homeassistant.components.lock import LockEntity
from the_keyspy import TheKeysLock

from .base import TheKeysEntity
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


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
        """Init a TheKeys lock entity."""
        super().__init__(device=device)

    def lock(self, **kwargs):
        """Lock the device."""
        self._device.close()
        self._attr_is_locked = True

    def unlock(self, **kwargs):
        """Unlock the device."""
        self._device.open()
        self._attr_is_locked = False

    def update(self) -> None:
        """Update the device."""
        try:
            self._device.retrieve_infos()
            self._attr_is_locked = self._device.is_locked
        except Exception as e:
            _LOGGER.error("Error updating lock: %s", e)
