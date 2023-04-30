
from homeassistant.components.sensor import SensorEntity

from ..update_coordinator import AerogardenUpdateCoordinator
from .aerogarden_entity import AerogardenEntity

class AerogardenSensor(AerogardenEntity, SensorEntity):
    def __init__(self, coordinator: AerogardenUpdateCoordinator, mac_addr: str, field: str, label=None, icon=None, unit=None):
        super().__init__(coordinator, mac_addr, field, label, icon)
        self._native_unit = unit
    
    @property
    def state(self):
        return self._native_state

    @property
    def native_unit_of_measurement(self):
        return self._native_unit

