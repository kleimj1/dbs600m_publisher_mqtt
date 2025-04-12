#!/usr/bin/env python3
import os
import time
import json
import threading
import tinytuya
import paho.mqtt.client as mqtt
from dps_metadata import DPS_METADATA

# Debug optional aktivieren
# tinytuya.set_debug()

# Umgebungsvariablen laden
DEVICE_ID = os.getenv("DEVICE_ID")
LOCAL_KEY = os.getenv("LOCAL_KEY")
DEVICE_IP = os.getenv("DEVICE_IP")
MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "dabbsson/dbs600m/status")
MQTT_COMMAND_TOPIC = os.getenv("MQTT_COMMAND_TOPIC", "dabbsson/dbs600m/command")
MQTT_DISCOVERY_PREFIX = os.getenv("MQTT_DISCOVERY_PREFIX", "homeassistant")
MQTT_USER = os.getenv("MQTT_USER", "")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "")

print("🚀 Starte Dabbsson DBS600M MQTT Publisher...")

# Tuya-Gerät initialisieren (OutletDevice für Wechselrichter)
try:
    device = tinytuya.OutletDevice(DEVICE_ID, DEVICE_IP, LOCAL_KEY)
    device.set_version(3.4)
except Exception as e:
    print(f"❌ Fehler beim Initialisieren des Geräts: {e}")
    exit(1)

# MQTT-Client vorbereiten
client = mqtt.Client()
if MQTT_USER:
    client.username_pw_set(MQTT_USER, MQTT_PASSWORD)

# Verbindungsaufbau-Callback
def on_connect(client, userdata, flags, rc):
    print(f"✅ MQTT verbunden (Code {rc})")
    client.subscribe(f"{MQTT_COMMAND_TOPIC}/#")

# Nachricht empfangen
def on_message(client, userdata, msg):
    try:
        dps_key = msg.topic.split("/")[-1]
        meta = DPS_METADATA.get(dps_key, {})
        if not meta.get("writable", False):
            print(f"⛔️ DPS {dps_key} ist nicht beschreibbar")
            return
        
        value = json.loads(msg.payload.decode())
        # Typkonvertierung für enum (z. B. Arbeitsmodus "0"/"1")
        if meta.get("type") == "enum" and isinstance(value, str):
            value = value.lower()  # Falls options als Kleinbuchstaben definiert sind
        
        print(f"➡️ Befehl für DPS {dps_key}: {value}")
        device.set_value(dps_key, value)
    except Exception as e:
        print(f"❌ Fehler bei Nachricht: {e}")

client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_HOST, MQTT_PORT, 60)

# Discovery-Payload für Home Assistant
def publish_discovery(dps_key):
    meta = DPS_METADATA.get(dps_key, {})
    if not meta:
        return

    name = meta.get("name", f"DPS {dps_key}")
    dtype = meta.get("type", "str")
    unit = meta.get("unit", "")
    writable = meta.get("writable", False)

    # Basis-Konfiguration
    device_config = {
        "identifiers": [f"dabbsson_dbs600m_{DEVICE_ID}"],
        "name": "Dabbsson DBS600M",
        "model": "DBS600M",
        "manufacturer": "Dabbsson"
    }

    payload = {
        "name": f"DBS600M {name}",
        "unique_id": f"dbs600m_{dps_key}_{DEVICE_ID}",
        "state_topic": f"{MQTT_TOPIC}/{dps_key}",
        "device": device_config
    }

    # Komponententyp bestimmen
    component = "sensor"
    if writable:
        if dtype == "bool":
            component = "switch"
            payload.update({
                "command_topic": f"{MQTT_COMMAND_TOPIC}/{dps_key}",
                "payload_on": "true",
                "payload_off": "false"
            })
        elif dtype == "int":
            component = "number"
            payload.update({
                "command_topic": f"{MQTT_COMMAND_TOPIC}/{dps_key}",
                "min": 0,
                "max": meta.get("max", 10000),  # Default-Werte anpassen
                "step": meta.get("step", 1)
            })
        elif dtype == "enum":
            component = "select"
            payload.update({
                "command_topic": f"{MQTT_COMMAND_TOPIC}/{dps_key}",
                "options": meta.get("options", [])
            })

    # Einheiten und Device-Klassen
    if unit:
        payload["unit_of_measurement"] = unit
        if unit == "W":
            payload["device_class"] = "power"
        elif unit == "V":
            payload["device_class"] = "voltage"
        elif unit == "A":
            payload["device_class"] = "current"
        elif unit == "°C":
            payload["device_class"] = "temperature"
        elif unit == "%":
            if "Batterie" in name:
                payload["device_class"] = "battery"

    # Discovery-Nachricht senden
    discovery_topic = f"{MQTT_DISCOVERY_PREFIX}/{component}/dbs600m_{dps_key}/config"
    print(f"🛰️ Discovery: {discovery_topic}")
    client.publish(discovery_topic, json.dumps(payload), retain=True)

# Status regelmäßig publizieren
def publish_loop():
    while True:
        try:
            data = device.status()
            dps = data.get("dps", {})
            print(f"🔍 Empfangene DPS-Daten: {dps}")
            
            for key, value in dps.items():
                if str(key) in DPS_METADATA:
                    # Wert für MQTT aufbereiten
                    if isinstance(value, bool):
                        val_str = "true" if value else "false"
                    else:
                        val_str = str(value)
                    
                    topic = f"{MQTT_TOPIC}/{key}"
                    client.publish(topic, val_str, retain=True)
                    publish_discovery(str(key))
        except Exception as e:
            print(f"⚠️ Fehler bei Statusabruf: {e}")
        time.sleep(10)  # Intervall anpassen

# Hauptprogramm
threading.Thread(target=publish_loop, daemon=True).start()
client.loop_forever()
