from paho.mqtt.enums import CallbackAPIVersion
from hasslorasensor.sensors.deviceinfo import DeviceInfo
from hasslorasensor.sensors.generic import LoraMqttSensor
from typing import List, Set
from paho.mqtt.client import Client
import logging
import json

class LoraMqttEventHandler:
    def __init__(self, sensors: List[LoraMqttSensor], mqtt_host_url: str, mqtt_port: int, mqtt_user: str = None, mqtt_pass:str = None, mqtt_keepalice: int = 60) -> None:
        self.sensors = {
            sensor.device_profile():sensor for sensor in sensors
        }

        self.client = Client(CallbackAPIVersion.VERSION2)

        def _on_connect(client, userdata, flags, reason_code, properties):
            self.client.subscribe("#")
        self.client.on_connect = _on_connect

        def _on_message(client, userdata, msg):
            self._handle_message(msg.topic, msg.payload)
        self.client.on_message = _on_message

        if mqtt_user is not None and mqtt_pass is not None:
            self.client.username_pw_set(mqtt_user, mqtt_pass)

        self.client.connect(mqtt_host_url, mqtt_port, mqtt_keepalice)

        self.devices: Set[str] = set()

    def run(self):
        self.client.loop_forever()

    def _discover_device(self, info: DeviceInfo):
        sensor = self.sensors.get(info.deviceProfileName)

        if sensor is None:
            logging.error(f"Unknown device profile name {info.deviceProfileName}")
            return

        self.devices.add(info.devEui)
        logging.info(f"Sending discovery message for {info.devEui} {info.deviceName}")
        messages = sensor.create_discovery_messages(info)
        for msg in messages:
            topic = f"homeassistant/sensor/{msg.name}/config"
            payload = json.dumps(msg.to_dict()).encode()
            self.client.publish(topic, payload)

    def _handle_message(self, topic: str, msg: bytes):
        logging.debug(f"Recevied: {topic} {msg}")

        if topic.startswith("application/"):
            payload = json.loads(msg.decode())
            info = DeviceInfo.from_dict(payload['deviceInfo'])

            if info.devEui not in self.devices:
                self._discover_device(info)



