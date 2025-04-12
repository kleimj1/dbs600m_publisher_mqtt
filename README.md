# 🚀 Dabbsson DBS600M MQTT Publisher – Home Assistant Add-on

Dieses Add-on liest über das Tuya-Protokoll (lokal via WLAN) **DPS-Werte vom Dabbsson DBS600M Wechselrichter** aus und veröffentlicht diese via **MQTT Discovery** an Home Assistant.  
**Vollständig lokal** – keine Cloud-Anbindung nötig!

---

## ✅ Funktionen
- ☀️ **PV-Daten**: Leistung, Spannung, Strom  
- 🔋 **Batterie-Status**: SoC, Temperatur  
- ⚡ **AC-Output**: Leistung, Ein/Aus-Schaltung  
- 🔧 **Steuerung**: Arbeitsmodus (Eco/Charge), Power Limit  
- 🧠 **Automatische Entitäten**: Sensoren & Schalter in HA  
- 📡 **Robuste LAN-Kommunikation** mit Wiederverbindung  

---

## 📦 Installation
1. Gehe in Home Assistant zu:  
   **Einstellungen → Add-ons → Add-on Store**  
2. Füge dieses Repository hinzu:  

https://github.com/kleimj1/dbs600m_mqtt_publisher

[![Add-on installieren](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https://github.com/kleimj1/dbs600m_mqtt_publisher)  
3. Installiere das Add-on **„Dabbsson DBS600M Publisher“** und konfiguriere es.

---

## ⚙️ Konfiguration
| Feld                   | Beschreibung                                  | Beispielwert       |
|------------------------|----------------------------------------------|--------------------|
| `device_id`            | Tuya Device ID (aus IoT-Portal)              | `123456789abc`     |
| `local_key`            | Tuya Local Key                               | `a1b2c3d4e5`       |
| `device_ip`            | Lokale IP des Wechselrichters                | `192.168.1.100`    |
| `mqtt_host`            | MQTT Broker (z. B. `core-mosquitto`)         | `core-mosquitto`   |
| `mqtt_port`            | Port (meist `1883`)                          | `1883`             |
| `mqtt_topic`           | Basis-Topic (Empfehlung: `dbs600m`)          | `dbs600m`          |

---

## 📡 MQTT Topics & Entitäten
### **Beispielhafte Topics:**
| Topic                     | Beschreibung               | Schreibbar | Einheit |
|---------------------------|----------------------------|------------|---------|
| `dbs600m/status/101`      | PV-Leistung                | ❌         | W       |
| `dbs600m/status/103`      | PV-Spannung                | ❌         | V       |
| `dbs600m/status/120`      | Batterie-SoC               | ❌         | %       |
| `dbs600m/status/108`      | Wechselrichter EIN/AUS     | ✅         | -       |
| `dbs600m/status/126`      | Arbeitsmodus (Eco/Charge)  | ✅         | -       |

### **Steuerung per MQTT:**
```bash
# Wechselrichter einschalten:
mosquitto_pub -h localhost -t dbs600m/command/108 -m "true"

# Arbeitsmodus auf "Charge" setzen:
mosquitto_pub -h localhost -t dbs600m/command/126 -m "1"

---

## 🔍 Device ID & Local Key ermitteln
Melde dich im Tuya IoT Portal an.

Erstelle ein Cloud-Projekt und verknüpfe dein Gerät.

Die Device ID und Local Key findest du in der Geräteübersicht.

## 🏠 Typische Home-Assistant-Entitäten
sensor.dbs600m_pv_leistung

sensor.dbs600m_batterie_soc

switch.dbs600m_wechselrichter

select.dbs600m_arbeitsmodus

## 🛠️ Technische Hinweise
Abfrageintervall: 10 Sekunden (schont das Gerät)

Discovery Prefix: homeassistant

DPS-Mapping: Vollständige Liste in dps_metadata.py

## ❤️ Beitrag & Support
Fehlt ein DPS-Wert oder hast du Verbesserungsvorschläge?
➡️ GitHub Issue erstellen

### 🔌 Viel Erfolg mit deinem DBS600M in Home Assistant!
