from typing import Any

from homeassistant.components.sensor import (SensorDeviceClass, SensorStateClass)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (PERCENTAGE,
                                 UnitOfElectricCurrent, UnitOfElectricPotential,
                                 UnitOfFrequency, UnitOfTime, UnitOfPower,
                                 UnitOfTemperature)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import DOMAIN
from .entities import BaseSensorEntity
from .mqtt.ecoflow_mqtt import EcoflowMQTTClient


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    client: EcoflowMQTTClient = hass.data[DOMAIN][entry.entry_id]

    from .devices.registry import devices
    async_add_entities(devices[client.device_type].sensors(client))


class CyclesSensorEntity(BaseSensorEntity):
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_icon = "mdi:battery-heart-variant"
    _attr_state_class = SensorStateClass.TOTAL_INCREASING


class FanSensorEntity(BaseSensorEntity):
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:fan"


class LevelSensorEntity(BaseSensorEntity):
    _attr_device_class = SensorDeviceClass.BATTERY
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_state_class = SensorStateClass.MEASUREMENT


class RemainSensorEntity(BaseSensorEntity):
    _attr_device_class = SensorDeviceClass.DURATION
    _attr_native_unit_of_measurement = UnitOfTime.MINUTES
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_value = 0

    def _update_value(self, val: Any) -> Any:
        ival = int(val)
        if ival < 0 or ival > 5000:
            ival = 0

        return super()._update_value(ival)


class TempSensorEntity(BaseSensorEntity):
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_value = -1


class VoltSensorEntity(BaseSensorEntity):
    _attr_device_class = SensorDeviceClass.VOLTAGE
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_native_unit_of_measurement = UnitOfElectricPotential.MILLIVOLT
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_value = 0


class AmpSensorEntity(BaseSensorEntity):
    _attr_device_class = SensorDeviceClass.CURRENT
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_native_unit_of_measurement = UnitOfElectricCurrent.MILLIAMPERE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_value = 0


class WattsSensorEntity(BaseSensorEntity):
    _attr_device_class = SensorDeviceClass.POWER
    _attr_native_unit_of_measurement = UnitOfPower.WATT
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_value = 0


class InWattsSensorEntity(WattsSensorEntity):
    _attr_icon = "mdi:transmission-tower-import"


class InWattsSolarSensorEntity(InWattsSensorEntity):
    def _update_value(self, val: Any) -> bool:
        return super()._update_value(int(val) / 10)


class OutWattsSensorEntity(WattsSensorEntity):
    _attr_icon = "mdi:transmission-tower-export"


class InVoltSensorEntity(VoltSensorEntity):
    _attr_icon = "mdi:transmission-tower-import"


class InAmpSensorEntity(AmpSensorEntity):
    _attr_icon = "mdi:transmission-tower-import"

class SolarWattsSensorEntity(WattsSensorEntity):
    _attr_icon = "mdi:mdi:solar-power"

class FrequencySensorEntity(BaseSensorEntity):
    _attr_device_class = SensorDeviceClass.FREQUENCY
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_native_unit_of_measurement = UnitOfFrequency.HERTZ
    _attr_state_class = SensorStateClass.MEASUREMENT