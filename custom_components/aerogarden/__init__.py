"""The aerogarden integration."""

import logging

from homeassistant.const import EVENT_HOMEASSISTANT_STOP
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed, ConfigEntryNotReady

from .const import DOMAIN
from .exceptions import HaAuthError, HaCannotConnect
from .update_coordinator import AerogardenUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict):
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up the aerogarden component."""
    hass.data.setdefault(DOMAIN, {})

    """Set up aerogarden from a config entry."""
    coordinator = AerogardenUpdateCoordinator(hass, entry)
    hass.data[DOMAIN][entry.entry_id] = coordinator

    try:
        if not await coordinator.async_setup():
            return False
    except HaCannotConnect:
        raise ConfigEntryNotReady("Could not connect to Aerogarden API")
    except HaAuthError:
        raise ConfigEntryAuthFailed("Could not authenticate to Aerogarden API")
        
    hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, coordinator.shutdown)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    coordinator: AerogardenUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    ok = await coordinator.async_reset()
    if ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return ok

async def async_update_options(hass: HomeAssistant, config_entry: ConfigEntry):
    """Update options."""
    await hass.config_entries.async_reload(config_entry.entry_id)