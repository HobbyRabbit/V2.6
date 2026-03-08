from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):

    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [
            ACInfinityTemperatureSensor(coordinator, entry.entry_id),
            ACInfinityHumiditySensor(coordinator, entry.entry_id),
        ]
    )


class ACInfinityTemperatureSensor(CoordinatorEntity, SensorEntity):

    _attr_native_unit_of_measurement = "°C"
    _attr_device_class = "temperature"

    def __init__(self, coordinator, entry_id):

        super().__init__(coordinator)

        self._attr_name = "AC Infinity Temperature"
        self._attr_unique_id = f"{entry_id}_temperature"

    @property
    def native_value(self):

        return self.coordinator.data.get("temperature")


class ACInfinityHumiditySensor(CoordinatorEntity, SensorEntity):

    _attr_native_unit_of_measurement = "%"
    _attr_device_class = "humidity"

    def __init__(self, coordinator, entry_id):

        super().__init__(coordinator)

        self._attr_name = "AC Infinity Humidity"
        self._attr_unique_id = f"{entry_id}_humidity"

    @property
    def native_value(self):

        return self.coordinator.data.get("humidity")
