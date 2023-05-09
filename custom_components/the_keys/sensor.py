from homeassistant.components.sensor import SensorDeviceClass, SensorEntity, SensorStateClass
from homeassistant.const import PERCENTAGE
from the_keyspy import TheKeysLock

from .base import TheKeysEntity
from .const import DOMAIN


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up TheKeys lock devices."""
    the_keys_api = hass.data[DOMAIN]

    entities = []

    for device in await hass.async_add_executor_job(the_keys_api.get_devices):
        if isinstance(device, TheKeysLock):
            entities.append(TheKeysLockBattery(device))

    async_add_entities(entities)


class TheKeysLockBattery(TheKeysEntity, SensorEntity):
    def __init__(self, device: TheKeysLock):
        super().__init__(device=device)
        self.type = "battery"
        self._device = device
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
        # usable_battery_level matches thekeys app
        return self._device.battery_level
