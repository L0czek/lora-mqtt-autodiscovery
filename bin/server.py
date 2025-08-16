#!/usr/bin/env python3

import argparse
import logging
from hasslorasensor.client import LoraMqttEventHandler
from hasslorasensor.sensors.lht65 import LHT65NSensor
import os

def main():
    parser = argparse.ArgumentParser("Homeassitant Lora Mqtt autodiscovery")
    parser.add_argument("--log-level", default='INFO', choices=logging.getLevelNamesMapping().keys())

    args = parser.parse_args()
    log_level = logging.getLevelName(args.log_level)
    logging.basicConfig(level=log_level)
    logging.info("Starting MQTT client")

    mqtt_host = os.environ.get("MQTT_HOST")
    mqtt_user = os.environ.get("MQTT_USER", None)
    mqtt_pass = os.environ.get("MQTT_PASS", None)

    if mqtt_host is None:
        logging.error("MQTT_HOST env variable is not defined")
        return

    mqtt_port = int(os.environ.get("MQTT_PORT", "1883"))
    mqtt_keepalive = int(os.environ.get("MQTT_KEEPALIVE", "60"))

    sensors = [
        LHT65NSensor()
    ]

    server = LoraMqttEventHandler(
        sensors=sensors,
        mqtt_host_url=mqtt_host,
        mqtt_port=mqtt_port,
        mqtt_user=mqtt_user,
        mqtt_pass=mqtt_pass,
        mqtt_keepalice=mqtt_keepalive
    )

    server.run()

if __name__ == "__main__":
    main()


