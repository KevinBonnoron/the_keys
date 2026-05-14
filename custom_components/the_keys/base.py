"""Base classes."""
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import (CoordinatorEntity,
                                                      DataUpdateCoordinator)
from the_keyspy import TheKeysDevice

from .const import DOMAIN


class TheKeysEntity(CoordinatorEntity):
    """Representation of a the_keys entity."""

    def __init__(self, coordinator: DataUpdateCoordinator, device: TheKeysDevice):
        """Init a TheKeys entity."""
        super().__init__(coordinator)
        self._device = device

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, str(device.id))},
            name=device.name,
            manufacturer="The Keys",
            model="Smart Lock",
        )

    @property
    def unique_id(self) -> str:
        """Return a unique ID."""
        return self._attr_unique_id
