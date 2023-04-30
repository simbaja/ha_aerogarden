"""Data update coordinator for Aerogarden"""

from datetime import timedelta

import asyncio
import logging
from .api import AerogardenApi, AerogardenAuthFailedError, AerogardenServerError
from .exceptions import HaAuthError, HaCannotConnect

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_SCAN_INTERVAL, CONF_PASSWORD, CONF_USERNAME
from homeassistant.helpers import aiohttp_client
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import (
    DOMAIN,
    DEFAULT_SCAN_INTERVAL
)

PLATFORMS = ["binary_sensor", "sensor", "light"]
_LOGGER = logging.getLogger(__name__)

class AerogardenUpdateCoordinator(DataUpdateCoordinator):
    """Define a wrapper class to update Aerogarden data."""

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        """Set up the AerogardenUpdateCoordinator class."""
        self._hass = hass
        self._session = aiohttp_client.async_get_clientsession(self.hass)
        self._config_entry = config_entry
        self._username = config_entry.data[CONF_USERNAME]
        self._password = config_entry.data[CONF_PASSWORD]
        self._api = AerogardenApi(self._session, self._username, self._password)

        options = config_entry.options
        self.update_interval = timedelta(seconds=options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL))

        super().__init__(hass, _LOGGER, name=DOMAIN)

    @property
    def api(self) -> AerogardenApi:
        return self._api

    async def async_setup(self):
        """Setup a new coordinator"""
        _LOGGER.debug("Setting up coordinator")

        try:
            await self._api.login()
            await self.async_config_entry_first_refresh()
        except AerogardenAuthFailedError:
            raise HaAuthError("Authentication failure")
        except AerogardenServerError:
            raise HaCannotConnect("Cannot connect (server error)")
        except Exception:
            raise HaCannotConnect("Unknown connection failure")        

        for component in PLATFORMS:
            self.hass.async_create_task(
                self.hass.config_entries.async_forward_entry_setup(
                    self._config_entry, component
                )
            )

        return True

    async def async_reset(self):
        """Resets the coordinator."""
        _LOGGER.debug("resetting the coordinator")
        entry = self._config_entry
        unload_ok = all(
            await asyncio.gather(
                *[
                    self.hass.config_entries.async_forward_entry_unload(
                        entry, component
                    )
                    for component in PLATFORMS
                ]
            )
        )
        return unload_ok

    async def _async_update_data(self):
        """Fetch the latest data from the source."""
        return await self._hass.async_add_executor_job(self._api.update())
