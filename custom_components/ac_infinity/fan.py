from __future__ import annotations

from homeassistant.components.fan import FanEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, DEFAULT_PORTS


async def async_setup_entry(hass, entry, async_add_entities):

    coordinator = hass.data[DOMAIN][entry.entry_id]

    entities = []

    for port in range(1, DEFAULT_PORTS + 1):
        entities.append(ACInfinityPortFan(coordinator, entry.entry_id, port))

    async_add_entities(entities)


class ACInfinityPortFan(CoordinatorEntity, FanEntity):

    def __init__(self, coordinator, entry_id, port):

        super().__init__(coordinator)

        self._port = port

        self._attr_name = f"AC Infinity Port {port}"
        self._attr_unique_id = f"{entry_id}_fan_port_{port}"

    @property
    def percentage(self):

        return self.coordinator.data["ports"].get(self._port, 0)

    async def async_set_percentage(self, percentage):

        await self.coordinator.set_port_speed(self._port, percentage)

    async def async_turn_on(self, percentage=None, preset_mode=None, **kwargs):

        if percentage is None:
            percentage = 100

        await self.coordinator.set_port_speed(self._port, percentage)

    async def async_turn_off(self, **kwargs):

        await self.coordinator.set_port_speed(self._port, 0)
