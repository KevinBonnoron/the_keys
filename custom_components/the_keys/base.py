"""Base classes."""
from homeassistant.helpers.entity import Entity
from the_keyspy import TheKeysDevice


class TheKeysEntity(Entity):
    """Representation of a the_keys entity."""

    def __init__(self, device: TheKeysDevice):
        """Init a TheKeys entity."""
        self._device = device
        self._attr_name = device.name

    @property
    def available(self) -> bool:
        """Return the available state."""
        return self._device is not None

    @property
    def unique_id(self) -> str:
        """Return a unique ID."""
        return self._device.id
