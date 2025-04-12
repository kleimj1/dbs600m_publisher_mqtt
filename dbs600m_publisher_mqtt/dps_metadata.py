DPS_METADATA = {
    # === PV-Daten ===
    "101": {
        "name": "PV-Leistung", 
        "type": "int", 
        "unit": "W", 
        "writable": False,
        "description": "Aktuelle PV-Eingangsleistung in Watt"
    },
    "103": {
        "name": "PV-Spannung", 
        "type": "int", 
        "unit": "V", 
        "writable": False,
        "description": "PV-Eingangsspannung in Volt"
    },
    "111": {
        "name": "PV-Strom", 
        "type": "int", 
        "unit": "A", 
        "writable": False,
        "description": "PV-Eingangsstrom in Ampere"
    },

    # === Systemzustände ===
    "104": {
        "name": "Inverter-Temp", 
        "type": "int", 
        "unit": "°C", 
        "writable": False,
        "description": "Temperatur des Wechselrichters"
    },
    "120": {
        "name": "Batterie SoC", 
        "type": "int", 
        "unit": "%", 
        "writable": False,
        "description": "Ladezustand der Batterie (State of Charge)"
    },
    "126": {
        "name": "Arbeitsmodus", 
        "type": "enum", 
        "options": ["0", "1"], 
        "writable": True,
        "description": "Modus: 0 = Eco (Netzeinspeisung), 1 = Ladung (Batteriepriorität)"
    },

    # === Leistungssteuerung ===
    "109": {
        "name": "AC Ausgang Leistung", 
        "type": "int", 
        "unit": "W", 
        "writable": False,
        "description": "Aktuelle AC-Ausgangsleistung in Watt"
    },
    "110": {
        "name": "Power Limit", 
        "type": "int", 
        "unit": "%", 
        "writable": True,
        "description": "Maximale Ausgangsleistung in Prozent (z. B. 80% für 800W bei 1000W-Inverter)"
    },

    # === Steuerbefehle ===
    "108": {
        "name": "Wechselrichter EIN/AUS", 
        "type": "bool", 
        "writable": True,
        "description": "Manuelles Ein-/Ausschalten des Wechselrichters"
    },
    "105": {
        "name": "Zähler zurücksetzen", 
        "type": "bool", 
        "writable": True,
        "description": "Setzt Energiezähler (kWh) zurück"
    }
}
