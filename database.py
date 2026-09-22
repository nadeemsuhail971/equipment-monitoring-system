from __future__ import annotations

import sqlite3
from typing import Any

import mysql.connector
from mysql.connector import Error as MySQLError

from src.config import DB_SETTINGS


def get_db_connection():
    """Return a MySQL connection when available; otherwise, fallback to SQLite."""
    if DB_SETTINGS.use_sqlite_fallback:
        try:
            import mysql.connector
            connection = mysql.connector.connect(
                host=DB_SETTINGS.host,
                port=DB_SETTINGS.port,
                user=DB_SETTINGS.user,
                password=DB_SETTINGS.password,
                database=DB_SETTINGS.database,
                autocommit=True,
            )
            return connection, "mysql"
        except MySQLError:
            pass

        sqlite_db = "equipment_monitoring.db"
        conn = sqlite3.connect(sqlite_db)
        return conn, "sqlite"

    try:
        connection = mysql.connector.connect(
            host=DB_SETTINGS.host,
            port=DB_SETTINGS.port,
            user=DB_SETTINGS.user,
            password=DB_SETTINGS.password,
            database=DB_SETTINGS.database,
            autocommit=True,
        )
        return connection, "mysql"
    except MySQLError as exc:
        raise RuntimeError(f"MySQL connection failed: {exc}") from exc


def initialize_database():
    conn, db_type = get_db_connection()
    if db_type == "sqlite":
        conn.execute("CREATE TABLE IF NOT EXISTS machines (machine_id INTEGER PRIMARY KEY AUTOINCREMENT, machine_name TEXT NOT NULL, machine_type TEXT NOT NULL, location TEXT NOT NULL, install_date TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'ACTIVE', created_at TEXT DEFAULT CURRENT_TIMESTAMP)")
        conn.execute("CREATE TABLE IF NOT EXISTS technicians (technician_id INTEGER PRIMARY KEY AUTOINCREMENT, technician_name TEXT NOT NULL, skill_area TEXT NOT NULL, phone TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP)")
        conn.execute("CREATE TABLE IF NOT EXISTS sensor_readings (reading_id INTEGER PRIMARY KEY AUTOINCREMENT, machine_id INTEGER NOT NULL, timestamp TEXT NOT NULL, temperature REAL NOT NULL, vibration REAL NOT NULL, pressure REAL NOT NULL, rpm INTEGER NOT NULL, running_hours REAL NOT NULL)")
        conn.execute("CREATE TABLE IF NOT EXISTS alerts (alert_id INTEGER PRIMARY KEY AUTOINCREMENT, machine_id INTEGER NOT NULL, alert_type TEXT NOT NULL, severity TEXT NOT NULL, message TEXT NOT NULL, created_at TEXT DEFAULT CURRENT_TIMESTAMP)")
        conn.execute("CREATE TABLE IF NOT EXISTS maintenance_logs (maintenance_id INTEGER PRIMARY KEY AUTOINCREMENT, machine_id INTEGER NOT NULL, technician_id INTEGER, maintenance_type TEXT NOT NULL, description TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'OPEN', created_at TEXT DEFAULT CURRENT_TIMESTAMP, scheduled_for TEXT)")
        conn.execute("CREATE TABLE IF NOT EXISTS machine_thresholds (threshold_id INTEGER PRIMARY KEY AUTOINCREMENT, machine_type TEXT NOT NULL, temp_warning REAL NOT NULL, temp_critical REAL NOT NULL, vibration_warning REAL NOT NULL, vibration_critical REAL NOT NULL, pressure_warning REAL NOT NULL, pressure_critical REAL NOT NULL, rpm_warning INTEGER NOT NULL, rpm_critical INTEGER NOT NULL, UNIQUE(machine_type))")
        conn.commit()
        return conn, db_type

    with conn.cursor() as cursor:
        cursor.execute("CREATE DATABASE IF NOT EXISTS equipment_monitoring")
        cursor.execute("USE equipment_monitoring")
    conn.commit()
    return conn, db_type


def insert_seed_data(conn, db_type):
    if db_type == "sqlite":
        cur = conn.cursor()
        cur.execute("INSERT OR IGNORE INTO machines (machine_id, machine_name, machine_type, location, install_date, status) VALUES (1, 'Press-01', 'Hydraulic Press', 'Plant A', '2021-08-15', 'ACTIVE')")
        cur.execute("INSERT OR IGNORE INTO machines (machine_id, machine_name, machine_type, location, install_date, status) VALUES (2, 'Boiler-07', 'Boiler', 'Plant B', '2019-04-10', 'ACTIVE')")
        cur.execute("INSERT OR IGNORE INTO machines (machine_id, machine_name, machine_type, location, install_date, status) VALUES (3, 'CNC-15', 'CNC Machine', 'Plant C', '2022-01-12', 'ACTIVE')")
        cur.execute("INSERT OR IGNORE INTO machines (machine_id, machine_name, machine_type, location, install_date, status) VALUES (4, 'Conv-09', 'Conveyor', 'Plant A', '2020-11-01', 'ACTIVE')")
        cur.execute("INSERT OR IGNORE INTO technicians (technician_id, technician_name, skill_area, phone) VALUES (1, 'Ava Chen', 'Mechanical Systems', '555-1001')")
        cur.execute("INSERT OR IGNORE INTO technicians (technician_id, technician_name, skill_area, phone) VALUES (2, 'Luis Gomez', 'Thermal Systems', '555-1002')")
        cur.execute("INSERT OR IGNORE INTO technicians (technician_id, technician_name, skill_area, phone) VALUES (3, 'Rina Patel', 'Electro-Mechanical', '555-1003')")
        cur.execute("INSERT OR IGNORE INTO machine_thresholds (threshold_id, machine_type, temp_warning, temp_critical, vibration_warning, vibration_critical, pressure_warning, pressure_critical, rpm_warning, rpm_critical) VALUES (1, 'Hydraulic Press', 75.0, 90.0, 6.0, 8.0, 130.0, 160.0, 1500, 1800)")
        cur.execute("INSERT OR IGNORE INTO machine_thresholds (threshold_id, machine_type, temp_warning, temp_critical, vibration_warning, vibration_critical, pressure_warning, pressure_critical, rpm_warning, rpm_critical) VALUES (2, 'Boiler', 120.0, 145.0, 7.0, 9.0, 180.0, 210.0, 1800, 2200)")
        cur.execute("INSERT OR IGNORE INTO machine_thresholds (threshold_id, machine_type, temp_warning, temp_critical, vibration_warning, vibration_critical, pressure_warning, pressure_critical, rpm_warning, rpm_critical) VALUES (3, 'CNC Machine', 72.0, 88.0, 5.5, 7.5, 105.0, 135.0, 1200, 1600)")
        cur.execute("INSERT OR IGNORE INTO machine_thresholds (threshold_id, machine_type, temp_warning, temp_critical, vibration_warning, vibration_critical, pressure_warning, pressure_critical, rpm_warning, rpm_critical) VALUES (4, 'Conveyor', 65.0, 80.0, 4.8, 6.5, 90.0, 120.0, 900, 1200)")
        conn.commit()
        return

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) as count FROM machines")
    if cursor.fetchone()["count"] == 0:
        cursor.execute("INSERT INTO machines (machine_name, machine_type, location, install_date, status) VALUES (%s, %s, %s, %s, %s)", ("Press-01", "Hydraulic Press", "Plant A", "2021-08-15", "ACTIVE"))
        cursor.execute("INSERT INTO machines (machine_name, machine_type, location, install_date, status) VALUES (%s, %s, %s, %s, %s)", ("Boiler-07", "Boiler", "Plant B", "2019-04-10", "ACTIVE"))
        cursor.execute("INSERT INTO machines (machine_name, machine_type, location, install_date, status) VALUES (%s, %s, %s, %s, %s)", ("CNC-15", "CNC Machine", "Plant C", "2022-01-12", "ACTIVE"))
        cursor.execute("INSERT INTO machines (machine_name, machine_type, location, install_date, status) VALUES (%s, %s, %s, %s, %s)", ("Conv-09", "Conveyor", "Plant A", "2020-11-01", "ACTIVE"))
        cursor.execute("INSERT INTO technicians (technician_name, skill_area, phone) VALUES (%s, %s, %s)", ("Ava Chen", "Mechanical Systems", "555-1001"))
        cursor.execute("INSERT INTO technicians (technician_name, skill_area, phone) VALUES (%s, %s, %s)", ("Luis Gomez", "Thermal Systems", "555-1002"))
        cursor.execute("INSERT INTO technicians (technician_name, skill_area, phone) VALUES (%s, %s, %s)", ("Rina Patel", "Electro-Mechanical", "555-1003"))
        conn.commit()


def fetch_all(cursor, query: str, params: tuple = ()):
    cursor.execute(query, params)
    return cursor.fetchall()


def close_connection(conn):
    if conn is not None:
        conn.close()
