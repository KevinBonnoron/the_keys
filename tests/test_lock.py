"""Test the lock entity."""

from unittest.mock import Mock

import pytest

from custom_components.the_keys.lock import TheKeysLockEntity


@pytest.mark.asyncio
async def test_lock_entity():
    """Test the lock entity."""
    mock_coordinator = Mock(last_update_success=True)
    mock_device = Mock()
    mock_device.name = "Test Lock"
    mock_device.id = "test_id"
    mock_device.is_locked = True

    entity = TheKeysLockEntity(mock_coordinator, mock_device)

    assert entity.unique_id == "test_id_lock"
    assert entity.is_locked is True

    entity.lock()
    mock_device.close.assert_called_once()

    entity.unlock()
    mock_device.open.assert_called_once()

    mock_device.is_locked = False
    assert entity.is_locked is False
