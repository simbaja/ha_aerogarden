import logging
from typing import Callable

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN
from .update_coordinator import AerogardenUpdateCoordinator
from .entities import AerogardenSensor

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities: Callable):
    """Aerogarden sensors."""

    _LOGGER.debug('Adding Aerogarden Sensor Entities')
    coordinator: AerogardenUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    sensors = []
    sensor_fields = {
        "plantedDay": 
        {
            "label": "Planted Days", 
            "icon": "mdi:calendar", 
            "unit": "Days"
        },
        "nutriRemindDay": {
            "label": "Nutrient Days",
            "icon": "mdi:calendar-clock",
            "unit": "Days",
        },
        "pumpLevel": {
            "label": "Pump Level",
            "icon": "mdi:water-percent",
            "unit": "Fill Level",
        },
    }

    for garden in coordinator.api.gardens:
        for field in sensor_fields.keys():
            s = sensor_fields[field]
            sensors.append(
                AerogardenSensor(
                    coordinator,
                    garden,
                    field,
                    label=s["label"],
                    icon=s["icon"],
                    unit=s["unit"],
                )
            )

    async_add_entities(sensors)
