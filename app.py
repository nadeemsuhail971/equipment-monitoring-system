from __future__ import annotations

import os
import sys
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

try:
    from src.analysis import calculate_health_score, evaluate_alerts
    from src.database import close_connection, get_db_connection, initialize_database, insert_seed_data
    from src.sensor_simulator import build_readings_for_machine
except ModuleNotFoundError:
    from analysis import calculate_health_score, evaluate_alerts
    from database import close_connection, get_db_connection, initialize_database, insert_seed_data
    from sensor_simulator import build_readings_for_machine


def fetch_machine_rows(conn, db_type):
    if db_type == "sqlite":
        cur = conn.cursor()
        cur.execute("SELECT machine_id, machine_name, machine_type, location, status FROM machines")
        return cur.fetchall()

    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT machine_id, machine_name, machine_type, location, status FROM machines")
    return cur.fetchall()


def insert_reading(conn, db_type, reading, machine_id):
    if db_type == "sqlite":
        conn.execute(
            "INSERT INTO sensor_readings (machine_id, timestamp, temperature, vibration, pressure, rpm, running_hours) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (machine_id, reading["timestamp"], reading["temperature"], reading["vibration"], reading["pressure"], reading["rpm"], reading["running_hours"]),
        )
        conn.commit()
        return

    cur = conn.cursor()
    cur.execute(
        "INSERT INTO sensor_readings (machine_id, timestamp, temperature, vibration, pressure, rpm, running_hours) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (machine_id, reading["timestamp"], reading["temperature"], reading["vibration"], reading["pressure"], reading["rpm"], reading["running_hours"]),
    )
    conn.commit()


def insert_alert(conn, db_type, machine_id, alert_type, severity, message):
    if db_type == "sqlite":
        conn.execute(
            "INSERT INTO alerts (machine_id, alert_type, severity, message, created_at) VALUES (?, ?, ?, ?, ?)",
            (machine_id, alert_type, severity, message, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        )
        conn.commit()
        return

    cur = conn.cursor()
    cur.execute(
        "INSERT INTO alerts (machine_id, alert_type, severity, message, created_at) VALUES (%s, %s, %s, %s, %s)",
        (machine_id, alert_type, severity, message, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
    )
    conn.commit()


def log_maintenance(conn, db_type, machine_id, technician_id, maintenance_type, description, status):
    if db_type == "sqlite":
        conn.execute(
            "INSERT INTO maintenance_logs (machine_id, technician_id, maintenance_type, description, status, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (machine_id, technician_id, maintenance_type, description, status, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        )
        conn.commit()
        return

    cur = conn.cursor()
    cur.execute(
        "INSERT INTO maintenance_logs (machine_id, technician_id, maintenance_type, description, status, created_at) VALUES (%s, %s, %s, %s, %s, %s)",
        (machine_id, technician_id, maintenance_type, description, status, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
    )
    conn.commit()


def run_demo():
    conn, db_type = get_db_connection()
    initialize_database()
    insert_seed_data(conn, db_type)

    machine_records = fetch_machine_rows(conn, db_type)
    print("\n=== Equipment Monitoring & Predictive Maintenance System ===")
    print("Database engine:", db_type.upper())
    print("Machines in system:")
    for machine in machine_records:
        print(f"- {machine[1]} [{machine[2]}] @ {machine[3]} | Status: {machine[4]}")

    for machine in machine_records:
        machine_id = machine[0]
        machine_name = machine[1]
        machine_type = machine[2]
        readings = build_readings_for_machine({"machine_name": machine_name, "machine_type": machine_type}, hours_back=3)

        for idx, reading in enumerate(readings[:6]):
            reading["history"] = readings[:idx + 1]
            # Keep each reading consistent over demo generation
            alerts = evaluate_alerts(reading, reading["thresholds"])
            health = calculate_health_score(reading, reading["thresholds"])
            insert_reading(conn, db_type, reading, machine_id)

            if alerts:
                print(f"\n[{machine_name}] Alert(s) detected: health={health}/100")
                for alert_type, severity, message in alerts:
                    print(f"  - {alert_type} [{severity}] {message}")
                    insert_alert(conn, db_type, machine_id, alert_type, severity, message)

                # Create maintenance log entry when critical alert is raised
                if any(severity == "CRITICAL" for _, severity, _ in alerts):
                    log_maintenance(conn, db_type, machine_id, 1, "Predictive Service", f"Critical issue detected on {machine_name}", "OPEN")

    print("\n=== Recent Alerts Summary ===")
    if db_type == "sqlite":
        cur = conn.cursor()
        cur.execute("SELECT machine_id, alert_type, severity, message, created_at FROM alerts ORDER BY alert_id DESC LIMIT 10")
        rows = cur.fetchall()
    else:
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT machine_id, alert_type, severity, message, created_at FROM alerts ORDER BY alert_id DESC LIMIT 10")
        rows = cur.fetchall()

    if rows:
        for row in rows:
            if db_type == "sqlite":
                machine_id, alert_type, severity, message, created_at = row
            else:
                machine_id, alert_type, severity, message, created_at = row["machine_id"], row["alert_type"], row["severity"], row["message"], row["created_at"]
            print(f"- Machine {machine_id}: {alert_type} | {severity} | {message} | {created_at}")
    else:
        print("No alerts generated.")

    print("\n=== Maintenance Log Summary ===")
    if db_type == "sqlite":
        cur.execute("SELECT machine_id, maintenance_type, status, description, created_at FROM maintenance_logs ORDER BY maintenance_id DESC LIMIT 10")
        logs = cur.fetchall()
    else:
        cur.execute("SELECT machine_id, maintenance_type, status, description, created_at FROM maintenance_logs ORDER BY maintenance_id DESC LIMIT 10")
        logs = cur.fetchall()

    if logs:
        for log in logs:
            if db_type == "sqlite":
                machine_id, maintenance_type, status, description, created_at = log
            else:
                machine_id, maintenance_type, status, description, created_at = log["machine_id"], log["maintenance_type"], log["status"], log["description"], log["created_at"]
            print(f"- Machine {machine_id}: {maintenance_type} | {status} | {description} | {created_at}")
    else:
        print("No maintenance tasks logged.")

    close_connection(conn)


if __name__ == "__main__":
    run_demo()
