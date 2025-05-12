"""Test the lock entity."""

from unittest.mock import Mock

import pytest

from custom_components.the_keys.lock import TheKeysLockEntity


@pytest.mark.asyncio
async def test_lock_entity():
    """Test the lock entity."""
    mock_device = Mock()
    mock_device.name = "Test Lock"
    mock_device.id = "test_id"
    mock_device.is_locked = True

    entity = TheKeysLockEntity(mock_device)

    assert entity.name == "Test Lock"
    assert entity.unique_id == "test_id"
    assert entity.available is True

    # Test lock operation
    entity.lock()
    mock_device.close.assert_called_once()
    assert entity.is_locked is True

    # Test unlock operation
    entity.unlock()
    mock_device.open.assert_called_once()
    assert entity.is_locked is False


@pytest.mark.asyncio
async def test_lock_update():
    """Test the lock update method."""
    mock_device = Mock()
    mock_device.is_locked = True

    entity = TheKeysLockEntity(mock_device)
    entity.update()

    mock_device.retrieve_infos.assert_called_once()
    assert entity.is_locked is True
