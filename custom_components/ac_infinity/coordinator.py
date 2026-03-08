from __future__ import annotations

import logging
import random

from datetime import timedelta

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.core import HomeAssistant

from .const import DOMAIN, DEFAULT_PORTS, SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)


class ACInfinityCoordinator(DataUpdateCoordinator):

    def __init__(self, hass: HomeAssistant, entry):

        self.hass = hass
        self.entry = entry

        self.address = entry.data.get("address", "unknown")

        self.ports = {p: 0 for p in range(1, DEFAULT_PORTS + 1)}
        self.power = {p: False for p in range(1, DEFAULT_PORTS + 1)}

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=SCAN_INTERVAL),
        )

    async def _async_update_data(self):

        # Replace with real BLE query later

        temperature = round(20 + random.random() * 5, 1)
        humidity = round(40 + random.random() * 10, 1)

        data = {
            "temperature": temperature,
            "humidity": humidity,
            "ports": self.ports,
            "power": self.power,
        }

        return data

    async def set_port_speed(self, port, speed):

        self.ports[port] = speed
        await self.async_request_refresh()

    async def set_port_power(self, port, state):

        self.power[port] = state
        await self.async_request_refresh()
