import asyncio
import logging
from bleak import BleakClient

SERVICE_UUID = "0000fff0-0000-1000-8000-00805f9b34fb"
WRITE_UUID = "0000fff2-0000-1000-8000-00805f9b34fb"
NOTIFY_UUID = "0000fff1-0000-1000-8000-00805f9b34fb"

_LOGGER = logging.getLogger(__name__)


class ACInfinityBLE:

    def __init__(self, address):

        self.address = address
        self.client = BleakClient(address)

        self.temperature = None
        self.humidity = None
        self.ports = {i: 0 for i in range(1, 9)}

        self._notify_event = asyncio.Event()

    async def connect(self):

        if self.client.is_connected:
            return

        await self.client.connect()

        await self.client.start_notify(
            NOTIFY_UUID,
            self._notification_handler,
        )

    def _notification_handler(self, sender, data):

        if data[0] != 0xAA or data[1] != 0x55:
            return

        cmd = data[3]

        if cmd == 0x20:
            self._parse_state(data)

        self._notify_event.set()

    def _parse_state(self, packet):

        temp_raw = (packet[4] << 8) | packet[5]

        self.temperature = temp_raw / 10
        self.humidity = packet[6]

        for i in range(8):
            self.ports[i + 1] = packet[7 + i]

    def _build_packet(self, cmd, payload):

        length = len(payload) + 1

        frame = bytearray([0xAA, 0x55, length, cmd])

        frame.extend(payload)

        checksum = sum(frame[2:]) & 0xFF

        frame.append(checksum)

        return frame

    async def request_state(self):

        packet = self._build_packet(0x10, [])

        self._notify_event.clear()

        await self.client.write_gatt_char(WRITE_UUID, packet)

        try:
            await asyncio.wait_for(self._notify_event.wait(), 5)
        except asyncio.TimeoutError:
            _LOGGER.warning("No response from controller")

        return {
            "temperature": self.temperature,
            "humidity": self.humidity,
            "ports": self.ports,
        }

    async def set_speed(self, port, speed):

        payload = bytearray([port, speed])

        packet = self._build_packet(0x11, payload)

        await self.client.write_gatt_char(WRITE_UUID, packet)

    async def set_power(self, port, state):

        payload = bytearray([port, 1 if state else 0])

        packet = self._build_packet(0x12, payload)

        await self.client.write_gatt_char(WRITE_UUID, packet)
