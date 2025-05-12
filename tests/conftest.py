"""Configuration for pytest."""

import os
import sys

import pytest
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from pytest_homeassistant_custom_component.common import MockConfigEntry

pytest_plugins = "pytest_asyncio"


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    """Enable custom integrations in Home Assistant."""
    yield


@pytest.fixture
def enable_custom_integrations(hass):
    """Enable custom integrations in Home Assistant."""
    hass.data.pop("custom_components", None)
    # Ensure custom components directory is in PYTHONPATH
    custom_components_dir = os.path.join(
        os.path.dirname(__file__), "../custom_components")
    if custom_components_dir not in sys.path:
        sys.path.insert(0, custom_components_dir)


@pytest.fixture
async def mock_the_keys_config_entry() -> ConfigEntry:
    """Return a mocked The Keys config entry."""
    return MockConfigEntry(
        domain="the_keys",
        data={
            CONF_USERNAME: "test-username",
            CONF_PASSWORD: "test-password",
        },
        entry_id="test",
    )


@pytest.fixture
async def hass(hass):
    """Fixture to provide a test instance of Home Assistant."""
    return hass
