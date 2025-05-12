"""Config flow for The Keys integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import (CONF_PASSWORD, CONF_SCAN_INTERVAL,
                                 CONF_USERNAME)
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import config_validation as cv
from the_keyspy import TheKeysApi

from .const import DEFAULT_SCAN_INTERVAL, DOMAIN, MIN_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_USERNAME): str,
        vol.Required(CONF_PASSWORD): str,
        vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): vol.All(cv.positive_int, vol.Clamp(min=MIN_SCAN_INTERVAL)),
    }
)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """

    # Validate phone number format
    username = data[CONF_USERNAME]
    if not username.startswith('+'):
        if username.startswith('0'):
            _LOGGER.debug(
                "Converting phone number starting with 0 to international format")
            username = '+33' + username[1:]
            data[CONF_USERNAME] = username
        else:
            _LOGGER.error("Phone number must start with + or 0")
            raise InvalidPhoneNumber

    if not username[1:].isdigit():
        _LOGGER.error("Phone number must contain only digits after the + sign")
        raise InvalidPhoneNumber

    try:
        api = await hass.async_add_executor_job(
            TheKeysApi, data[CONF_USERNAME], data[CONF_PASSWORD]
        )
        await hass.async_add_executor_job(api.get_devices)
    except Exception as err:
        _LOGGER.error("Error when setting up The Keys API: %s", err)
        raise CannotConnect from err

    return {
        CONF_USERNAME: data[CONF_USERNAME],
        CONF_PASSWORD: data[CONF_PASSWORD],
        CONF_SCAN_INTERVAL: data[CONF_SCAN_INTERVAL],
    }


async def async_migrate_entry(hass: HomeAssistant, config_entry: config_entries.ConfigEntry) -> bool:
    """Migrate old entry to new."""
    pass


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for The Keys."""

    VERSION = 1
    MINOR_VERSION = 1

    async def async_step_import(self, import_config):
        """Import a config entry from configuration.yaml."""
        return await self.async_step_user(import_config)

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidPhoneNumber:
                errors["base"] = "invalid_phone_number"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(title=info[CONF_USERNAME], data=info)

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidPhoneNumber(HomeAssistantError):
    """Error to indicate the phone number is invalid."""
