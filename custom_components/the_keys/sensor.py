"""Sensor platform for the_keys."""
from homeassistant.components.sensor import (SensorDeviceClass, SensorEntity,
                                             SensorStateClass)
from homeassistant.const import PERCENTAGE
from the_keyspy import TheKeysLock

from .base import TheKeysEntity
from .const import DOMAIN


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up TheKeys battery sensors."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    if not coordinator.data:
        return

    entities = []
    for device in coordinator.data:
        if isinstance(device, TheKeysLock):
            if device.battery_level is not None:
                entities.append(TheKeysLockBattery(coordinator, device))

    async_add_entities(entities, update_before_add=True)


class TheKeysLockBattery(TheKeysEntity, SensorEntity):
    """TheKeys battery device implementation."""

    def __init__(self, coordinator, device: TheKeysLock):
        """Init a TheKeys battery entity."""
        super().__init__(device=device)
        self._attr_unique_id = f"{self._device.id}_battery"
        self._attr_device_class = SensorDeviceClass.BATTERY
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = PERCENTAGE
        self._attr_icon = "mdi:battery"

    @staticmethod
    def has_battery() -> bool:
        """Return whether the device has a battery."""
        return True

    @property
    def native_value(self) -> int:
        """Return battery level."""
        return self._device.battery_level
