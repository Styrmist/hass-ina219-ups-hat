"""INA219 UPS Hat sensors."""

import logging

from homeassistant import core
from homeassistant.components.sensor import SensorEntity
from homeassistant.components.sensor.const import SensorDeviceClass, SensorStateClass
from homeassistant.const import (
    PERCENTAGE,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfPower,
    UnitOfTime,
)
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .coordinator import INA219UpsHatCoordinator
from .entity import INA219UpsHatEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(
    hass: core.HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    # We only want this platform to be set up via discovery.
    if discovery_info is None:
        return

    coordinator = discovery_info.get("coordinator")

    sensors = [
        VoltageSensor(coordinator),
        CurrentSensor(coordinator),
        PowerSensor(coordinator),
        ReadPowerSensor(coordinator),
        SocSensor(coordinator),
        SocInuSensor(coordinator),
        RemainingCapacitySensor(coordinator),
        RemainingTimeSensor(coordinator),
        RemainingTimeCustomSensor(coordinator),
    ]
    async_add_entities(sensors)


class INA219UpsHatSensor(INA219UpsHatEntity, SensorEntity):
    """Base sensor."""

    def __init__(self, coordinator: INA219UpsHatCoordinator) -> None:
        super().__init__(coordinator)
        self._attr_suggested_display_precision = 2


class VoltageSensor(INA219UpsHatSensor):
    def __init__(self, coordinator) -> None:
        super().__init__(coordinator)
        self._name = "Voltage"
        self._attr_native_unit_of_measurement = UnitOfElectricPotential.VOLT
        self._attr_device_class = SensorDeviceClass.VOLTAGE

    @property
    def native_value(self):
        return self._coordinator.data["voltage"]


class CurrentSensor(INA219UpsHatSensor):
    def __init__(self, coordinator) -> None:
        super().__init__(coordinator)
        self._name = "Current"
        self._attr_native_unit_of_measurement = UnitOfElectricCurrent.AMPERE
        self._attr_device_class = SensorDeviceClass.CURRENT

    @property
    def native_value(self):
        return self._coordinator.data["current"]


class PowerSensor(INA219UpsHatSensor):
    def __init__(self, coordinator) -> None:
        super().__init__(coordinator)
        self._name = "Power"
        self._attr_native_unit_of_measurement = UnitOfPower.WATT
        self._attr_device_class = SensorDeviceClass.POWER

    @property
    def native_value(self):
        return self._coordinator.data["power"]

class ReadPowerSensor(INA219UpsHatSensor):
    def __init__(self, coordinator) -> None:
        super().__init__(coordinator)
        self._name = "Read Power"
        self._attr_native_unit_of_measurement = UnitOfPower.WATT
        self._attr_device_class = SensorDeviceClass.POWER

    @property
    def native_value(self):
        return self._coordinator.data["read_power"]


class SocSensor(INA219UpsHatSensor):
    def __init__(self, coordinator) -> None:
        super().__init__(coordinator)
        self._name = "SoC"
        self._attr_native_unit_of_measurement = PERCENTAGE
        self._attr_device_class = SensorDeviceClass.BATTERY
        self._attr_suggested_display_precision = 1

    @property
    def native_value(self):
        return self._coordinator.data["soc"]

class SocInuSensor(INA219UpsHatSensor):
    def __init__(self, coordinator) -> None:
        super().__init__(coordinator)
        self._name = "SoC Inu"
        self._attr_native_unit_of_measurement = PERCENTAGE
        self._attr_device_class = SensorDeviceClass.BATTERY
        self._attr_suggested_display_precision = 1

    @property
    def native_value(self):
        return self._coordinator.data["soc_inu"]

class RemainingCapacitySensor(INA219UpsHatSensor):
    def __init__(self, coordinator) -> None:
        super().__init__(coordinator)
        self._name = "Remaining Capacity"
        self._attr_native_unit_of_measurement = UnitOfEnergy.WATT_HOUR
        self._attr_device_class = SensorDeviceClass.ENERGY_STORAGE
        self._attr_suggested_display_precision = 0

    @property
    def native_value(self):
        return self._coordinator.data["remaining_battery_capacity"]


class RemainingTimeSensor(INA219UpsHatSensor):
    def __init__(self, coordinator) -> None:
        super().__init__(coordinator)
        self._name = "Remaining Time"
        self._attr_native_unit_of_measurement = UnitOfTime.HOURS
        self._attr_device_class = SensorDeviceClass.DURATION
        self._attr_state_class = SensorStateClass.TOTAL_INCREASING
        self._attr_suggested_display_precision = 0

    @property
    def native_unit_of_measurement(self):
        remaining_hours = self._coordinator.data.get("remaining_time")
        if remaining_hours is None or remaining_hours >= 1:
            return UnitOfTime.HOURS
        return UnitOfTime.MINUTES

    @property
    def native_value(self):
        remaining_hours = self._coordinator.data.get("remaining_time")
        if remaining_hours is None:
            return None
        if remaining_hours >= 1:
            return remaining_hours
        # For short durations, show minutes instead of fractions of an hour.
        return remaining_hours * 60

class RemainingTimeCustomSensor(INA219UpsHatSensor):
    def __init__(self, coordinator) -> None:
        super().__init__(coordinator)
        self._name = "Remaining Time Custom"
        self._attr_native_unit_of_measurement = UnitOfTime.HOURS
        self._attr_device_class = SensorDeviceClass.DURATION
        self._attr_state_class = SensorStateClass.TOTAL_INCREASING
        self._attr_suggested_display_precision = 0

    @property
    def native_unit_of_measurement(self):
        remaining_hours = self._coordinator.data.get("remaining_time_custom")
        if remaining_hours is None or remaining_hours >= 1:
            return UnitOfTime.HOURS
        return UnitOfTime.MINUTES

    @property
    def native_value(self):
        remaining_hours = self._coordinator.data.get("remaining_time_custom")
        if remaining_hours is None:
            return None
        if remaining_hours >= 1:
            return remaining_hours
        # For short durations, show minutes instead of fractions of an hour.
        return remaining_hours * 60
