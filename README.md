# Equipment Monitoring & Predictive Maintenance System

This project simulates an industrial equipment monitoring system that collects machine sensor data, stores it in a database, checks thresholds for abnormal behavior, and triggers maintenance alerts before failures happen.

## Features

- Simulated sensor readings for temperature, vibration, pressure, RPM, and running hours
- MySQL-ready schema with indexing on machine and timestamp
- SQLite fallback for local execution without MySQL
- Threshold-based alert detection
- Trend-based detection using recent change checks
- Health scoring for machine condition
- Maintenance logging

## Project Structure

```text
equipment_monitoring_system/
├── db/
│   └── schema.sql
├── src/
│   ├── __init__.py
│   ├── app.py
│   ├── analysis.py
│   ├── config.py
│   ├── database.py
│   └── sensor_simulator.py
├── requirements.txt
├── README.md
└── equipment_monitoring.db   # created when SQLite fallback is used
```

## Setup

```powershell
cd "C:\Users\Amir suhail\equipment_monitoring_system"
python -m pip install -r requirements.txt
python src/app.py
```

## MySQL Setup

Set environment variables before running:

```powershell
$env:DB_HOST="localhost"
$env:DB_PORT="3306"
$env:DB_USER="root"
$env:DB_PASSWORD="your_password"
$env:DB_NAME="equipment_monitoring"
$env:USE_SQLITE_FALLBACK="0"
python src/app.py
```

## Output Example

```text
=== Equipment Monitoring & Predictive Maintenance System ===
Database engine: SQLITE
Machines in system:
- Press-01 [Hydraulic Press] @ Plant A | Status: ACTIVE
- Boiler-07 [Boiler] @ Plant B | Status: ACTIVE
- CNC-15 [CNC Machine] @ Plant C | Status: ACTIVE
- Conv-09 [Conveyor] @ Plant A | Status: ACTIVE

[Press-01] Alert(s) detected: health=93.7/100
  - PRESSURE [WARNING] Pressure 140.58 psi exceeds warning limit 130.0 psi.
  - TREND [WARNING] Rapid trend change indicates possible developing fault.
```
