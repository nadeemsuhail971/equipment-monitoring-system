from __future__ import annotations

import random
from datetime import datetime, timedelta

from src.config import MACHINE_SEED, THRESHOLD_LOOKUP


MACHINE_TYPE_BASE = {
    "Hydraulic Press": {"temperature": 62, "vibration": 3.2, "pressure": 110, "rpm": 1250, "running_hours": 320.0},
    "Boiler": {"temperature": 108, "vibration": 4.6, "pressure": 150, "rpm": 1600, "running_hours": 510.0},
    "CNC Machine": {"temperature": 58, "vibration": 2.8, "pressure": 90, "rpm": 980, "running_hours": 240.0},
    "Conveyor": {"temperature": 51, "vibration": 2.1, "pressure": 76, "rpm": 700, "running_hours": 420.0},
}


def generate_sensor_reading(machine_name: str, machine_type: str, timestamp: datetime | None = None):
    base = MACHINE_TYPE_BASE[machine_type]
    if timestamp is None:
        timestamp = datetime.now()

    temp_offset = random.uniform(-4, 8)
    vibration_offset = random.uniform(-0.6, 1.2)
    pressure_offset = random.uniform(-8, 14)
    rpm_offset = random.randint(-120, 220)
    running_hours = base["running_hours"] + random.uniform(0.2, 1.5)

    thresholds = THRESHOLD_LOOKUP[machine_type]
    temperature = max(0, base["temperature"] + temp_offset)
    vibration = max(0.5, base["vibration"] + vibration_offset)
    pressure = max(20, base["pressure"] + pressure_offset)
    rpm = max(0, base["rpm"] + rpm_offset)

    if random.random() < 0.18:
        temperature += random.uniform(8, 15)
    if random.random() < 0.15:
        vibration += random.uniform(1.4, 3.1)
    if random.random() < 0.12:
        pressure += random.uniform(12, 24)
    if random.random() < 0.10:
        rpm += random.randint(180, 420)

    if machine_name.lower().startswith("press") and random.random() < 0.07:
        temperature += random.uniform(10, 20)
        vibration += random.uniform(1.0, 2.5)

    return {
        "machine_name": machine_name,
        "machine_type": machine_type,
        "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        "temperature": round(temperature, 2),
        "vibration": round(vibration, 2),
        "pressure": round(pressure, 2),
        "rpm": int(rpm),
        "running_hours": round(running_hours, 2),
        "thresholds": {
            "temp_warning": thresholds.temp_warning,
            "temp_critical": thresholds.temp_critical,
            "vibration_warning": thresholds.vibration_warning,
            "vibration_critical": thresholds.vibration_critical,
            "pressure_warning": thresholds.pressure_warning,
            "pressure_critical": thresholds.pressure_critical,
            "rpm_warning": thresholds.rpm_warning,
            "rpm_critical": thresholds.rpm_critical,
        },
    }


def build_readings_for_machine(machine_record, hours_back=6):
    machine_name = machine_record["machine_name"]
    machine_type = machine_record["machine_type"]
    readings = []
    current_time = datetime.now()

    for step in range(hours_back * 4):
        ts = current_time - timedelta(minutes=15 * step)
        readings.append(generate_sensor_reading(machine_name, machine_type, ts))

    return readings


def get_seed_machines():
    return MACHINE_SEED
