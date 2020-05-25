"""Provides device automations for Sagemcom."""
from typing import List, Optional

import voluptuous as vol

from homeassistant.const import (
    ATTR_ENTITY_ID,
    CONF_DEVICE_ID,
    CONF_DOMAIN,
    CONF_ENTITY_ID,
    CONF_TYPE,
    SERVICE_RELOAD,
)
from homeassistant.core import Context, HomeAssistant
from homeassistant.helpers import entity_registry
import homeassistant.helpers.config_validation as cv

from . import DOMAIN

# TODO specify your supported action types.
ACTION_TYPES = {"reboot"}

ACTION_SCHEMA = cv.DEVICE_ACTION_BASE_SCHEMA.extend(
    {
        vol.Required(CONF_TYPE): vol.In(ACTION_TYPES),
        vol.Required(CONF_ENTITY_ID): cv.entity_domain(DOMAIN),
    }
)


async def async_get_actions(hass: HomeAssistant, device_id: str) -> List[dict]:
    """List device actions for Sagemcom devices."""
    registry = await entity_registry.async_get_registry(hass)
    actions = []

    # TODO Read this comment and remove it.
    # This example shows how to iterate over the entities of this device
    # that match this integration. If your actions instead rely on
    # calling services, do something like:
    # zha_device = await _async_get_zha_device(hass, device_id)
    # return zha_device.device_actions

    # Get all the integrations entities for this device
    for entry in entity_registry.async_entries_for_device(registry, device_id):
        if entry.domain != DOMAIN:
            continue

        print(entry)

        # Add actions for each entity that belongs to this integration
        # TODO add your own actions.
        actions.append(
            {
                CONF_DEVICE_ID: device_id,
                CONF_DOMAIN: DOMAIN,
                CONF_ENTITY_ID: entry.entity_id,
                CONF_TYPE: "reboot",
            }
        )

    return actions


async def async_call_action_from_config(
    hass: HomeAssistant, config: dict, variables: dict, context: Optional[Context]
) -> None:
    """Execute a device action."""
    config = ACTION_SCHEMA(config)

    service_data = {ATTR_ENTITY_ID: config[CONF_ENTITY_ID]}

    if config[CONF_TYPE] == "reboot":
        service = SERVICE_RELOAD

    await hass.services.async_call(
        DOMAIN, service, service_data, blocking=True, context=context
    )