from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class DBConfig:
    host: str = os.getenv("DB_HOST", "localhost")
    port: int = int(os.getenv("DB_PORT", "3306"))
    user: str = os.getenv("DB_USER", "root")
    password: str = os.getenv("DB_PASSWORD", "")
    database: str = os.getenv("DB_NAME", "equipment_monitoring")
    use_sqlite_fallback: bool = os.getenv("USE_SQLITE_FALLBACK", "1") == "1"


@dataclass
class SensorThresholds:
    temp_warning: float = 75.0
    temp_critical: float = 90.0
    vibration_warning: float = 6.0
    vibration_critical: float = 8.0
    pressure_warning: float = 120.0
    pressure_critical: float = 150.0
    rpm_warning: int = 1400
    rpm_critical: int = 1700


DB_SETTINGS = DBConfig()

MACHINE_TYPES = {
    "Hydraulic Press": "Hydraulic Press",
    "Boiler": "Boiler",
    "CNC Machine": "CNC Machine",
    "Conveyor": "Conveyor",
}

THRESHOLD_LOOKUP = {
    "Hydraulic Press": SensorThresholds(75.0, 90.0, 6.0, 8.0, 130.0, 160.0, 1500, 1800),
    "Boiler": SensorThresholds(120.0, 145.0, 7.0, 9.0, 180.0, 210.0, 1800, 2200),
    "CNC Machine": SensorThresholds(72.0, 88.0, 5.5, 7.5, 105.0, 135.0, 1200, 1600),
    "Conveyor": SensorThresholds(65.0, 80.0, 4.8, 6.5, 90.0, 120.0, 900, 1200),
}

MACHINE_SEED = [
    {"machine_name": "Press-01", "machine_type": "Hydraulic Press", "location": "Plant A", "install_date": "2021-08-15"},
    {"machine_name": "Boiler-07", "machine_type": "Boiler", "location": "Plant B", "install_date": "2019-04-10"},
    {"machine_name": "CNC-15", "machine_type": "CNC Machine", "location": "Plant C", "install_date": "2022-01-12"},
    {"machine_name": "Conv-09", "machine_type": "Conveyor", "location": "Plant A", "install_date": "2020-11-01"},
]

TECHNICIAN_SEED = [
    {"technician_name": "Ava Chen", "skill_area": "Mechanical Systems", "phone": "555-1001"},
    {"technician_name": "Luis Gomez", "skill_area": "Thermal Systems", "phone": "555-1002"},
    {"technician_name": "Rina Patel", "skill_area": "Electro-Mechanical", "phone": "555-1003"},
]
