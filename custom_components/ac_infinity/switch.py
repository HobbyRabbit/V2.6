from __future__ import annotations

from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, DEFAULT_PORTS


async def async_setup_entry(hass, entry, async_add_entities):

    coordinator = hass.data[DOMAIN][entry.entry_id]

    entities = []

    for port in range(1, DEFAULT_PORTS + 1):
        entities.append(ACInfinityPortSwitch(coordinator, entry.entry_id, port))

    async_add_entities(entities)


class ACInfinityPortSwitch(CoordinatorEntity, SwitchEntity):

    def __init__(self, coordinator, entry_id, port):

        super().__init__(coordinator)

        self._port = port

        self._attr_name = f"AC Infinity Port {port} Power"
        self._attr_unique_id = f"{entry_id}_switch_port_{port}"

    @property
    def is_on(self):

        return self.coordinator.data["power"].get(self._port, False)

    async def async_turn_on(self, **kwargs):

        await self.coordinator.set_port_power(self._port, True)

    async def async_turn_off(self, **kwargs):

        await self.coordinator.set_port_power(self._port, False)
