CREATE DATABASE IF NOT EXISTS equipment_monitoring;
USE equipment_monitoring;

CREATE TABLE IF NOT EXISTS machines (
    machine_id INT AUTO_INCREMENT PRIMARY KEY,
    machine_name VARCHAR(100) NOT NULL,
    machine_type VARCHAR(50) NOT NULL,
    location VARCHAR(100) NOT NULL,
    install_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS technicians (
    technician_id INT AUTO_INCREMENT PRIMARY KEY,
    technician_name VARCHAR(100) NOT NULL,
    skill_area VARCHAR(100) NOT NULL,
    phone VARCHAR(30),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sensor_readings (
    reading_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    machine_id INT NOT NULL,
    timestamp DATETIME NOT NULL,
    temperature DECIMAL(6,2) NOT NULL,
    vibration DECIMAL(6,2) NOT NULL,
    pressure DECIMAL(6,2) NOT NULL,
    rpm INT NOT NULL,
    running_hours DECIMAL(8,2) NOT NULL,
    INDEX idx_machine_timestamp (machine_id, timestamp),
    INDEX idx_timestamp (timestamp),
    CONSTRAINT fk_sensor_machine FOREIGN KEY (machine_id) REFERENCES machines(machine_id)
);

CREATE TABLE IF NOT EXISTS alerts (
    alert_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    machine_id INT NOT NULL,
    alert_type VARCHAR(50) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_alert_machine_time (machine_id, created_at),
    CONSTRAINT fk_alert_machine FOREIGN KEY (machine_id) REFERENCES machines(machine_id)
);

CREATE TABLE IF NOT EXISTS maintenance_logs (
    maintenance_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    machine_id INT NOT NULL,
    technician_id INT,
    maintenance_type VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'OPEN',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    scheduled_for DATETIME,
    INDEX idx_maintenance_machine_time (machine_id, created_at),
    CONSTRAINT fk_maintenance_machine FOREIGN KEY (machine_id) REFERENCES machines(machine_id),
    CONSTRAINT fk_maintenance_tech FOREIGN KEY (technician_id) REFERENCES technicians(technician_id)
);

CREATE TABLE IF NOT EXISTS machine_thresholds (
    threshold_id INT AUTO_INCREMENT PRIMARY KEY,
    machine_type VARCHAR(50) NOT NULL,
    temp_warning DECIMAL(6,2) NOT NULL,
    temp_critical DECIMAL(6,2) NOT NULL,
    vibration_warning DECIMAL(6,2) NOT NULL,
    vibration_critical DECIMAL(6,2) NOT NULL,
    pressure_warning DECIMAL(6,2) NOT NULL,
    pressure_critical DECIMAL(6,2) NOT NULL,
    rpm_warning INT NOT NULL,
    rpm_critical INT NOT NULL,
    UNIQUE KEY uq_machine_type (machine_type)
);

INSERT INTO machine_thresholds (machine_type, temp_warning, temp_critical, vibration_warning, vibration_critical, pressure_warning, pressure_critical, rpm_warning, rpm_critical)
VALUES
('Hydraulic Press', 78.0, 92.0, 6.5, 8.8, 140.0, 170.0, 1500, 1800),
('Boiler', 120.0, 145.0, 7.2, 9.2, 180.0, 210.0, 1800, 2200),
('CNC Machine', 72.0, 88.0, 5.5, 7.6, 110.0, 140.0, 1200, 1600),
('Conveyor', 65.0, 80.0, 4.8, 6.9, 95.0, 120.0, 900, 1200)
ON DUPLICATE KEY UPDATE
    temp_warning = VALUES(temp_warning),
    temp_critical = VALUES(temp_critical),
    vibration_warning = VALUES(vibration_warning),
    vibration_critical = VALUES(vibration_critical),
    pressure_warning = VALUES(pressure_warning),
    pressure_critical = VALUES(pressure_critical),
    rpm_warning = VALUES(rpm_warning),
    rpm_critical = VALUES(rpm_critical);
