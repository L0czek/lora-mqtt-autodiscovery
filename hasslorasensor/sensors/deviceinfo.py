from dataclasses import dataclass, field
from typing import Dict
from uuid import UUID
from enum import Enum
import json

class DeviceClass(str, Enum):
    CLASS_A = "CLASS_A"
    CLASS_B = "CLASS_B"
    CLASS_C = "CLASS_C"

@dataclass
class DeviceInfo:
    tenantId: UUID
    tenantName: str
    applicationId: UUID
    applicationName: str
    deviceProfileId: UUID
    deviceProfileName: str
    deviceName: str
    devEui: str
    deviceClassEnabled: DeviceClass
    tags: Dict[str, str] = field(default_factory=dict)

    @staticmethod
    def from_dict(data: dict) -> "DeviceInfo":
        return DeviceInfo(
            tenantId=UUID(data["tenantId"]),
            tenantName=data["tenantName"],
            applicationId=UUID(data["applicationId"]),
            applicationName=data["applicationName"],
            deviceProfileId=UUID(data["deviceProfileId"]),
            deviceProfileName=data["deviceProfileName"],
            deviceName=data["deviceName"],
            devEui=data["devEui"],
            deviceClassEnabled=DeviceClass(data["deviceClassEnabled"]),
            tags=data.get("tags", {})
        )

    def to_dict(self) -> dict:
        return {
            "tenantId": str(self.tenantId),
            "tenantName": self.tenantName,
            "applicationId": str(self.applicationId),
            "applicationName": self.applicationName,
            "deviceProfileId": str(self.deviceProfileId),
            "deviceProfileName": self.deviceProfileName,
            "deviceName": self.deviceName,
            "devEui": self.devEui,
            "deviceClassEnabled": self.deviceClassEnabled.value,
            "tags": self.tags
        }

# Optional: JSON helpers
    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @staticmethod
    def from_json(json_str: str) -> "DeviceInfo":
        return DeviceInfo.from_dict(json.loads(json_str))
