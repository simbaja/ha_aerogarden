
from homeassistant.components.light import LightEntity

from ..update_coordinator import AerogardenUpdateCoordinator
from .aerogarden_entity import AerogardenEntity

class AerogardenLight(AerogardenEntity, LightEntity):
    def __init__(self, coordinator: AerogardenUpdateCoordinator, mac_addr: str):
        super().__init__(coordinator, mac_addr, "lightStat", "Light")
    
    @property
    def is_on(self):
        return self._native_state != 0

    async def async_turn_on(self, **kwargs):
        await self._api.light_toggle(self._macaddr)

    async def async_turn_off(self, **kwargs):
        await self._api.light_toggle(self._macaddr)