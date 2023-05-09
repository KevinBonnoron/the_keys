from homeassistant.helpers.entity import Entity
from the_keyspy import TheKeysDevice

from .const import DOMAIN


class TheKeysEntity(Entity):
    """Representation of a the_keys entity"""

    def __init__(self, device: TheKeysDevice):
        """Init a TheKeys entity."""
        self._device = device

    @property
    def available(self):
        """Return the available state."""
        return self._device.status()

    @property
    def unique_id(self) -> str:
        """Return a unique ID."""
        return self._device.id

    @property
    def device_info(self):
        """Return the device_info of the device."""
        return {
            "identifiers": {(DOMAIN, self.unique_id)},
            "manufacturer": "The Keys",
            "name": self.name,
            "device_type": "Lock",
        }
