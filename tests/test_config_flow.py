"""Test the config flow."""

from unittest.mock import patch

import pytest
from homeassistant import config_entries
from homeassistant.const import (CONF_PASSWORD, CONF_SCAN_INTERVAL,
                                 CONF_USERNAME)
from the_keyspy.errors import TheKeysApiError

from custom_components.the_keys.config_flow import CannotConnect
from custom_components.the_keys.const import CONF_GATEWAY_IP, DEFAULT_SCAN_INTERVAL, DOMAIN

VALID_PHONE = "+33612345678"


@pytest.mark.asyncio
async def test_form(hass):
    """Test we get the form."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == "form"
    assert result["errors"] == {}

    with patch(
        "custom_components.the_keys.config_flow.TheKeysApi.get_devices",
        return_value=[],
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_USERNAME: VALID_PHONE,
                CONF_PASSWORD: "test-password",
            },
        )
        await hass.async_block_till_done()

    assert result2["type"] == "create_entry"
    assert result2["title"] == VALID_PHONE
    assert result2["data"] == {
        CONF_USERNAME: VALID_PHONE,
        CONF_PASSWORD: "test-password",
        CONF_SCAN_INTERVAL: DEFAULT_SCAN_INTERVAL,
        CONF_GATEWAY_IP: None,
    }


@pytest.mark.asyncio
async def test_form_invalid_auth(hass):
    """Test we handle invalid auth."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "custom_components.the_keys.config_flow.validate_input",
        side_effect=CannotConnect,
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_USERNAME: VALID_PHONE,
                CONF_PASSWORD: "test-password",
                CONF_SCAN_INTERVAL: DEFAULT_SCAN_INTERVAL,
            },
        )

    assert result2["type"] == "form"
    assert result2["errors"] == {"base": "cannot_connect"}


@pytest.mark.asyncio
async def test_form_with_gateway_ip(hass):
    """Test config flow with a gateway IP provided."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "custom_components.the_keys.config_flow.TheKeysApi.get_devices",
        return_value=[],
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_USERNAME: VALID_PHONE,
                CONF_PASSWORD: "test-password",
                CONF_GATEWAY_IP: "192.168.1.100",
            },
        )
        await hass.async_block_till_done()

    assert result2["type"] == "create_entry"
    assert result2["data"][CONF_GATEWAY_IP] == "192.168.1.100"


@pytest.mark.asyncio
async def test_form_with_empty_gateway_ip(hass):
    """Test config flow without gateway IP stores None."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "custom_components.the_keys.config_flow.TheKeysApi.get_devices",
        return_value=[],
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_USERNAME: VALID_PHONE,
                CONF_PASSWORD: "test-password",
            },
        )
        await hass.async_block_till_done()

    assert result2["type"] == "create_entry"
    assert result2["data"][CONF_GATEWAY_IP] is None


@pytest.mark.asyncio
async def test_form_with_invalid_gateway_ip(hass):
    """Test config flow rejects invalid gateway IP."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    result2 = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {
            CONF_USERNAME: VALID_PHONE,
            CONF_PASSWORD: "test-password",
            CONF_GATEWAY_IP: "not-an-ip",
        },
    )

    assert result2["type"] == "form"
    assert result2["errors"] == {"base": "invalid_gateway_ip"}


@pytest.mark.asyncio
async def test_form_api_error(hass):
    """Test we handle TheKeysApiError as cannot_connect."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "custom_components.the_keys.config_flow.TheKeysApi.get_devices",
        side_effect=TheKeysApiError("API error"),
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_USERNAME: VALID_PHONE,
                CONF_PASSWORD: "test-password",
                CONF_SCAN_INTERVAL: DEFAULT_SCAN_INTERVAL,
            },
        )

    assert result2["type"] == "form"
    assert result2["errors"] == {"base": "cannot_connect"}
