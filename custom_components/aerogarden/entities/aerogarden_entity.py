from typing import Optional, Dict, Any

from homeassistant.helpers.update_coordinator import CoordinatorEntity
from ..api import AerogardenApi
from ..update_coordinator import AerogardenUpdateCoordinator
from ..const import DOMAIN 

class AerogardenEntity(CoordinatorEntity):
    """Base class for all Aerogarden Entities"""

    def __init__(self, coordinator: AerogardenUpdateCoordinator, mac_addr: str, field: str, label=None, icon=None):
        super.__init__(coordinator)

        self._api = coordinator.api
        self._mac_addr = mac_addr
        self._field = field
        self._label = label
        if not label:
            self._label = field
        self._icon = icon
        self._garden_name = self._api.garden_name(self._macaddr)
        self._name = f"{self._garden_name} {self._label}"

    @property
    def unique_id(self) -> Optional[str]:
        return f"{DOMAIN}_{self.mac_addr.lower()}_{self._field.lower()}"

    @property
    def api(self) -> AerogardenApi:
        return self._api

    @property
    def device_info(self) -> Dict:
        """Device info dictionary."""

        return {
            "identifiers": {(DOMAIN, self.mac_addr)},
            "name": self._garden_name,
            "manufacturer": "Aerogarden"
        }

    @property
    def mac_addr(self) -> str:
        return self._mac_addr

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def icon(self) -> Optional[str]:
        return self._get_icon()

    @property
    def device_class(self) -> Optional[str]:
        return self._get_device_class() 

    @property
    def _native_state(self):
        return self._get_state()

    def _get_state(self):
        return self._api.garden_property(self._mac_addr, self._field)

    def _get_icon(self) -> Optional[str]:
        return self._icon

    def _get_device_class(self) -> Optional[str]:
        return None
