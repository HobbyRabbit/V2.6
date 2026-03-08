import logging
from datetime import timedelta

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN, SCAN_INTERVAL, PORTS
from .ble_controller import ACInfinityBLE

_LOGGER = logging.getLogger(__name__)


class ACInfinityCoordinator(DataUpdateCoordinator):

    def __init__(self, hass, entry):

        self.address = entry.data["address"]

        self.ble = ACInfinityBLE(self.address)

        self.ports = {p: 0 for p in range(1, PORTS + 1)}
        self.power = {p: False for p in range(1, PORTS + 1)}

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=SCAN_INTERVAL),
        )
    async def _async_update_data(self):

        await self.ble.connect()

        state = await self.ble.request_state()

        return state

        return {
            "temperature": state["temperature"],
            "humidity": state["humidity"],
            "ports": self.ports,
            "power": self.power,
        }

    async def set_port_speed(self, port, speed):

        await self.ble.set_speed(port, speed)

        self.ports[port] = speed

        await self.async_request_refresh()

    async def set_port_power(self, port, state):

        await self.ble.set_power(port, state)

        self.power[port] = state

        await self.async_request_refresh()
