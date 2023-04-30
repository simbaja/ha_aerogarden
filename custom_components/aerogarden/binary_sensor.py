import logging
from typing import Callable

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN
from .update_coordinator import AerogardenUpdateCoordinator
from .entities import AerogardenBinarySensor

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities: Callable):
    """Aerogarden binary sensors."""

    _LOGGER.debug('Adding Aerogarden Binary Sensor Entities')
    coordinator: AerogardenUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    sensors = []
    sensor_fields = {
        "pumpStat": {
            "label": "Pump",
            "icon": "mdi:water-pump",
        },
        "nutriStatus": {
            "label": "Needs Nutrients",
            "icon": "mdi:cup-water",
        },
        "pumpHydro": {
            "label": "Needs Water",
            "icon": "mdi:water",
        },
    }

    for garden in coordinator.api.gardens:
        for field in sensor_fields.keys():
            s = sensor_fields[field]
            sensors.append(
                AerogardenBinarySensor(
                    coordinator, garden, field, label=s["label"], icon=s["icon"]
                )
            )

    async_add_entities(sensors)
