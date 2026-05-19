-- PhishGuard Database Schema
-- Auto-created by the application on startup

CREATE DATABASE IF NOT EXISTS phishguard_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_general_ci;

USE phishguard_db;

-- Scan records table: stores all URL and message scan results
CREATE TABLE IF NOT EXISTS scan_records (
    scan_id INT AUTO_INCREMENT PRIMARY KEY,
    scan_type ENUM('URL', 'SMS', 'Email') NOT NULL,
    submitted_content TEXT NOT NULL,
    prediction VARCHAR(50) NOT NULL,
    risk_score FLOAT DEFAULT 0.0,
    threat_level VARCHAR(20) DEFAULT 'Safe',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_scan_type (scan_type),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB;

-- Threat reasons table: stores explanation reasons for each scan
CREATE TABLE IF NOT EXISTS threat_reasons (
    reason_id INT AUTO_INCREMENT PRIMARY KEY,
    scan_id INT NOT NULL,
    reason_text TEXT NOT NULL,
    FOREIGN KEY (scan_id) REFERENCES scan_records(scan_id)
        ON DELETE CASCADE,
    INDEX idx_scan_id (scan_id)
) ENGINE=InnoDB;
