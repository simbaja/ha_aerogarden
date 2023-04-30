"""Data update coordinator for Aerogarden"""

import asyncio
import logging
from .api import AerogardenApi, AerogardenAuthFailedError, AerogardenServerError
from .exceptions import HaAuthError, HaCannotConnect

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import (
    DOMAIN,
    MIN_TIME_BETWEEN_UPDATES
)

PLATFORMS = ["binary_sensor", "sensor", "light"]
_LOGGER = logging.getLogger(__name__)

class AerogardenUpdateCoordinator(DataUpdateCoordinator):
    """Define a wrapper class to update Aerogarden data."""

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        """Set up the AerogardenUpdateCoordinator class."""
        self._hass = hass
        self._config_entry = config_entry
        self._username = config_entry.data[CONF_USERNAME]
        self._password = config_entry.data[CONF_PASSWORD]
        self._api = AerogardenApi(self._username, self._password)
        self.update_interval = MIN_TIME_BETWEEN_UPDATES

        super().__init__(hass, _LOGGER, name=DOMAIN)

    @property
    def api(self) -> AerogardenApi:
        return self._api

    async def async_setup(self):
        """Setup a new coordinator"""
        _LOGGER.debug("Setting up coordinator")

        try:
            await self._hass.async_add_executor_job(self._api.login())
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
