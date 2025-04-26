from typing import List
from hasslorasensor.sensors.deviceinfo import DeviceInfo
from dataclasses import dataclass
from typing import List
from enum import Enum

class DeviceClass(str, Enum):
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    VOLTAGE = "voltage"

    def unit(self) -> str:
        if self.value == "temperature":
            return "°C"
        elif self.value == "humidity":
            return "%"
        else:
            return "V"

@dataclass
class Measurement:
    id: str
    device_class: DeviceClass

@dataclass
class Device:
    name: str
    identifiers: List[str]

@dataclass
class HassMqttSensor:
    name: str
    state_topic: str
    device_class: DeviceClass
    value_template: str
    unique_id: str
    device: Device

    @staticmethod
    def from_dict(data: dict) -> "HassMqttSensor":
        return HassMqttSensor(
            name=data["name"],
            state_topic=data["state_topic"],
            device_class=DeviceClass(data["device_class"]),
            value_template=data["value_template"],
            unique_id=data["unique_id"],
            device=Device(
                name=data["device"]["name"],
                identifiers=data["device"].get("identifiers", [])
            )
        )

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "state_topic": self.state_topic,
            "device_class": self.device_class.value,
            "unit_of_measurement": self.device_class.unit(),
            "value_template": self.value_template,
            "unique_id": self.unique_id,
            "device": {
                "name": self.device.name,
                "identifiers": self.device.identifiers
            }
        }

class LoraMqttSensor():
    def __init__(self) -> None:
        pass

    def device_profile(self) -> str:
        raise NotImplemented

    def create_discovery_messages(self, info: DeviceInfo) -> List[HassMqttSensor]:
        raise NotImplemented

    def state_topic_event_up(self, info: DeviceInfo) -> str:
        return f"application/{info.applicationId}/device/{info.devEui}/event/up"

    def state_topic_join(self, info: DeviceInfo) -> str:
        return f"application/{info.applicationId}/device/{info.devEui}/event/join"

    def device(self, info: DeviceInfo) -> Device:
        return Device(name=info.deviceName, identifiers=[info.devEui])



