"""Base classes."""
from homeassistant.helpers.entity import DeviceInfo, Entity
from the_keyspy import TheKeysDevice

from .const import DOMAIN


class TheKeysEntity(Entity):
    """Representation of a the_keys entity."""

    def __init__(self, device: TheKeysDevice):
        """Init a TheKeys entity."""
        self._device = device

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, str(device.id))},
            name=device.name,
            manufacturer="The Keys",
            model="Smart Lock",
        )

    @property
    def available(self) -> bool:
        """Return the available state."""
        return self._device is not None

    @property
    def unique_id(self) -> str:
        """Return a unique ID."""
        return self._attr_unique_id
