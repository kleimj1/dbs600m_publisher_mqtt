#!/bin/sh

# Konfiguration aus /data/options.json setzen
export DEVICE_ID=$(jq -r .device_id /data/options.json)
export LOCAL_KEY=$(jq -r .local_key /data/options.json)
export DEVICE_IP=$(jq -r .device_ip /data/options.json)
export MQTT_HOST=$(jq -r .mqtt_host /data/options.json)
export MQTT_PORT=$(jq -r .mqtt_port /data/options.json)
export MQTT_TOPIC=$(jq -r .mqtt_topic /data/options.json)
export MQTT_COMMAND_TOPIC=$(jq -r .mqtt_command_topic /data/options.json)
export MQTT_DISCOVERY_PREFIX=$(jq -r .mqtt_discovery_prefix /data/options.json)
export MQTT_USER=$(jq -r .mqtt_user /data/options.json)
export MQTT_PASSWORD=$(jq -r .mqtt_password /data/options.json)

# Starte Skript in venv
/venv/bin/python /mqtt_publisher.py
