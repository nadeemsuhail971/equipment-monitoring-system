from __future__ import annotations

from datetime import datetime


def calculate_trend(readings):
    if len(readings) < 2:
        return 0.0
    latest = readings[-1]
    previous = readings[-2]
    delta = {
        "temperature": latest["temperature"] - previous["temperature"],
        "vibration": latest["vibration"] - previous["vibration"],
        "pressure": latest["pressure"] - previous["pressure"],
        "rpm": latest["rpm"] - previous["rpm"],
    }
    return delta


def evaluate_alerts(reading, thresholds):
    alerts = []
    if reading["temperature"] >= thresholds["temp_critical"]:
        alerts.append(("TEMPERATURE", "CRITICAL", f"Temperature {reading['temperature']}C exceeds critical limit {thresholds['temp_critical']}C."))
    elif reading["temperature"] >= thresholds["temp_warning"]:
        alerts.append(("TEMPERATURE", "WARNING", f"Temperature {reading['temperature']}C exceeds warning limit {thresholds['temp_warning']}C."))

    if reading["vibration"] >= thresholds["vibration_critical"]:
        alerts.append(("VIBRATION", "CRITICAL", f"Vibration {reading['vibration']} mm/s exceeds critical limit {thresholds['vibration_critical']} mm/s."))
    elif reading["vibration"] >= thresholds["vibration_warning"]:
        alerts.append(("VIBRATION", "WARNING", f"Vibration {reading['vibration']} mm/s exceeds warning limit {thresholds['vibration_warning']} mm/s."))

    if reading["pressure"] >= thresholds["pressure_critical"]:
        alerts.append(("PRESSURE", "CRITICAL", f"Pressure {reading['pressure']} psi exceeds critical limit {thresholds['pressure_critical']} psi."))
    elif reading["pressure"] >= thresholds["pressure_warning"]:
        alerts.append(("PRESSURE", "WARNING", f"Pressure {reading['pressure']} psi exceeds warning limit {thresholds['pressure_warning']} psi."))

    if reading["rpm"] >= thresholds["rpm_critical"]:
        alerts.append(("RPM", "CRITICAL", f"RPM {reading['rpm']} exceeds critical limit {thresholds['rpm_critical']} rpm."))
    elif reading["rpm"] >= thresholds["rpm_warning"]:
        alerts.append(("RPM", "WARNING", f"RPM {reading['rpm']} exceeds warning limit {thresholds['rpm_warning']} rpm."))

    history = reading["history"] if "history" in reading else [reading]
    if len(history) >= 2:
        trend = calculate_trend(history)
        rate_change = any(abs(value) > 12 for value in trend.values())
        if rate_change:
            alerts.append(("TREND", "WARNING", "Rapid trend change indicates possible developing fault."))

    return alerts


def calculate_health_score(reading, thresholds):
    score = 100
    score -= max(0, reading["temperature"] - thresholds["temp_warning"]) * 1.4
    score -= max(0, reading["vibration"] - thresholds["vibration_warning"]) * 8
    score -= max(0, reading["pressure"] - thresholds["pressure_warning"]) * 0.6
    score -= max(0, reading["rpm"] - thresholds["rpm_warning"]) * 0.03
    score = max(0, min(100, round(score, 1)))
    return score


def format_alert_message(machine_name, alert_type, severity, description):
    return f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {machine_name}: {alert_type} {severity} - {description}"
