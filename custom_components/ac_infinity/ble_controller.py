import logging
from bleak import BleakClient

from .const import WRITE_UUID, READ_UUID

_LOGGER = logging.getLogger(__name__)


class ACInfinityBLE:

    def __init__(self, address):

        self.address = address
        self.client = None

    async def connect(self):

        if self.client and self.client.is_connected:
            return

        self.client = BleakClient(self.address)
        await self.client.connect()

    async def disconnect(self):

        if self.client and self.client.is_connected:
            await self.client.disconnect()

    async def read_state(self):

        await self.connect()

        raw = await self.client.read_gatt_char(READ_UUID)

        # Example decode (depends on controller firmware)
        temperature = raw[4] + raw[5] / 10
        humidity = raw[6]

        return {
            "temperature": temperature,
            "humidity": humidity,
        }

    async def set_speed(self, port, speed):

        await self.connect()

        command = bytearray([0xA5, port, speed])

        await self.client.write_gatt_char(WRITE_UUID, command)

    async def set_power(self, port, state):

        await self.connect()

        command = bytearray([0xA6, port, 1 if state else 0])

        await self.client.write_gatt_char(WRITE_UUID, command)
