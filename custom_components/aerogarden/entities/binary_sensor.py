
from homeassistant.components.binary_sensor import BinarySensorEntity

from ..update_coordinator import AerogardenUpdateCoordinator
from .aerogarden_entity import AerogardenEntity

class AerogardenBinarySensor(AerogardenEntity, BinarySensorEntity):
    def __init__(self, coordinator: AerogardenUpdateCoordinator, mac_addr: str, field: str, label=None, icon=None):
        super().__init__(coordinator, mac_addr, field, label, icon)
    
    @property
    def is_on(self):
        return self._native_state != 0

