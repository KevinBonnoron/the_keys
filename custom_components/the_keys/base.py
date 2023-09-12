from homeassistant.helpers.entity import Entity
from the_keyspy import TheKeysDevice

from .const import DOMAIN


class TheKeysEntity(Entity):
    """Representation of a the_keys entity"""

    def __init__(self, device: TheKeysDevice):
        """Init a TheKeys entity."""
        self._device = device
        self._attr_unique_id = f"{device.id} {self.type}"
        self._attr_name = self.type.capitalize()

    @property
    def available(self) -> bool:
        """Return the available state."""
        return self._device is not None

    @property
    def unique_id(self) -> str:
        """Return a unique ID."""
        return self._device.id

    @property
    def type(self) -> str:
        return None
