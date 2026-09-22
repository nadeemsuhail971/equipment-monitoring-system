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
