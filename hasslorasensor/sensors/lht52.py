from typing import List
from hasslorasensor.sensors.generic import DeviceClass, LoraMqttSensor, HassMqttSensor, Measurement, DeviceInfo

class LHT52NSensor(LoraMqttSensor):
    def __init__(self) -> None:
        super().__init__()

        self.measurements = {
            "battery_voltage": Measurement(id="Bat_mV", device_class=DeviceClass.VOLTAGE, unit="mV"),
            "internal_temp_sensor": Measurement(id="TempC_SHT", device_class=DeviceClass.TEMPERATURE),
            "humidity_sensor": Measurement(id="Hum_SHT", device_class=DeviceClass.HUMIDITY)
        }

    def device_profile(self) -> str:
        return "LHT52"

    def create_discovery_messages(self, info: DeviceInfo) -> List[HassMqttSensor]:
        return [
            HassMqttSensor(
                name=f"{name}_{info.deviceName}",
                state_topic=super().state_topic_event_up(info),
                device_class=measurement.device_class,
                value_template="{{" + f"value_json.object.{measurement.id}" + "}}",
                unique_id=f"{name}_{info.devEui}",
                device=super().device(info),
                unit=measurement.unit
            )
                for name, measurement in self.measurements.items()
        ]
