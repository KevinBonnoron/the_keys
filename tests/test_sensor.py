"""Test the sensor entity."""

from unittest.mock import Mock

import pytest
from homeassistant.const import PERCENTAGE

from custom_components.the_keys.sensor import TheKeysLockBattery


@pytest.mark.asyncio
async def test_battery_sensor():
    """Test the battery sensor entity."""
    mock_device = Mock()
    mock_device.name = "Test Battery"
    mock_device.id = "test_battery_id"
    mock_device.battery_level = 75

    entity = TheKeysLockBattery(mock_device)

    assert entity.name == "Test Battery"
    assert entity.unique_id == "test_battery_id"
    assert entity.native_unit_of_measurement == PERCENTAGE
    assert entity.native_value == 75
    assert entity.has_battery() is True
