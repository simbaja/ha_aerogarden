import logging
from typing import Callable

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN
from .update_coordinator import AerogardenUpdateCoordinator
from .entities import AerogardenLight

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities: Callable):
    """Aerogarden lights"""

    _LOGGER.debug('Adding Aerogarden Light Entities')
    coordinator: AerogardenUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    lights = []

    for garden in coordinator.api.gardens:
        lights.append(AerogardenLight(coordinator, garden))

    async_add_entities(lights)
