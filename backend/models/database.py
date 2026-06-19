"""PhishGuard Database Connection Layer

Provides MySQL database connection management and query methods.
Auto-creates database and tables on initialization.
All queries use parameterized statements for SQL injection prevention.
"""

import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG


class Database:
    """MySQL database manager for PhishGuard scan records."""

    def __init__(self):
        """Initialize database connection and auto-create schema."""
        self._init_database()

    def _get_connection(self):
        """Create and return a new database connection.
        
        Returns:
            mysql.connector.connection: Active MySQL connection
        """
        return mysql.connector.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database=DB_CONFIG['database'],
            charset=DB_CONFIG['charset'],
            collation=DB_CONFIG['collation']
        )

    def _init_database(self):
        """Auto-create database and tables if they don't exist.
        
        First connects without database name to create the database,
        then reconnects with database name to create tables.
        """
        try:
            # Step 1: Connect without database to create it
            conn = mysql.connector.connect(
                host=DB_CONFIG['host'],
                port=DB_CONFIG['port'],
                user=DB_CONFIG['user'],
                password=DB_CONFIG['password']
            )
            cursor = conn.cursor()

            # Create database (cannot use parameterized query for DB name)
            cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']} "
                f"CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci"
            )
            conn.commit()
            cursor.close()
            conn.close()

            # Step 2: Connect WITH database to create tables
            conn = self._get_connection()
            cursor = conn.cursor()

            # Create scan_records table
            cursor.execute("""
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
                ) ENGINE=InnoDB
            """)

            # Create threat_reasons table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS threat_reasons (
                    reason_id INT AUTO_INCREMENT PRIMARY KEY,
                    scan_id INT NOT NULL,
                    reason_text TEXT NOT NULL,
                    FOREIGN KEY (scan_id) REFERENCES scan_records(scan_id)
                        ON DELETE CASCADE,
                    INDEX idx_scan_id (scan_id)
                ) ENGINE=InnoDB
            """)

            conn.commit()
            cursor.close()
            conn.close()
            print("[DB] Database 'phishguard_db' initialized successfully.")

        except Error as e:
            print(f"[DB] Warning: Could not initialize database: {e}")
            print("[DB] Make sure MySQL (XAMPP) is running.")

    def save_scan(self, scan_type, content, prediction, risk_score, threat_level, reasons):
        """Save a scan result with associated threat reasons.
        
        Args:
            scan_type: Type of scan ('URL', 'SMS', 'Email')
            content: The submitted URL or message text
            prediction: Classification result ('Safe', 'Suspicious', 'Phishing', 'Scam')
            risk_score: Numeric risk score (0.0 - 100.0)
            threat_level: Threat level string ('Safe', 'Low', 'Medium', 'High', 'Critical')
            reasons: List of explanation reason strings
        
        Returns:
            int: The scan_id of the saved record, or None if save failed
        """
        conn = None
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            # Insert scan record using parameterized query
            cursor.execute(
                "INSERT INTO scan_records (scan_type, submitted_content, prediction, risk_score, threat_level) "
                "VALUES (%s, %s, %s, %s, %s)",
                (scan_type, content, prediction, risk_score, threat_level)
            )
            scan_id = cursor.lastrowid

            # Insert threat reasons using parameterized query
            if reasons:
                for reason in reasons:
                    cursor.execute(
                        "INSERT INTO threat_reasons (scan_id, reason_text) VALUES (%s, %s)",
                        (scan_id, reason)
                    )

            conn.commit()
            cursor.close()
            return scan_id

        except Error as e:
            print(f"[DB] Error saving scan: {e}")
            if conn:
                conn.rollback()
            return None

        finally:
            if conn and conn.is_connected():
                conn.close()

    def get_scan(self, scan_id):
        """Get a detailed scan record with its threat reasons.
        
        Args:
            scan_id: The ID of the scan to retrieve
        
        Returns:
            dict: Scan record with reasons, or None if not found
        """
        conn = None
        try:
            conn = self._get_connection()
            cursor = conn.cursor(dictionary=True)

            # Get scan record using parameterized query
            cursor.execute(
                "SELECT * FROM scan_records WHERE scan_id = %s",
                (scan_id,)
            )
            scan = cursor.fetchone()

            if not scan:
                cursor.close()
                return None

            # Convert datetime to string for JSON serialization
            if scan.get('created_at'):
                scan['created_at'] = scan['created_at'].isoformat()

            # Get threat reasons using parameterized query
            cursor.execute(
                "SELECT reason_text FROM threat_reasons WHERE scan_id = %s",
                (scan_id,)
            )
            reasons = [row['reason_text'] for row in cursor.fetchall()]
            scan['reasons'] = reasons

            cursor.close()
            return scan

        except Error as e:
            print(f"[DB] Error getting scan: {e}")
            return None

        finally:
            if conn and conn.is_connected():
                conn.close()

    def get_history(self, limit=50, offset=0):
        """Get paginated scan history.
        
        Args:
            limit: Maximum number of records to return (default 50)
            offset: Number of records to skip (default 0)
        
        Returns:
            list: List of scan record dicts
        """
        conn = None
        try:
            conn = self._get_connection()
            cursor = conn.cursor(dictionary=True)

            # Get scan records ordered by most recent, using parameterized query
            cursor.execute(
                "SELECT * FROM scan_records ORDER BY created_at DESC LIMIT %s OFFSET %s",
                (limit, offset)
            )
            records = cursor.fetchall()

            # Convert datetime to string for JSON serialization
            for record in records:
                if record.get('created_at'):
                    record['created_at'] = record['created_at'].isoformat()

            cursor.close()
            return records

        except Error as e:
            print(f"[DB] Error getting history: {e}")
            return []

        finally:
            if conn and conn.is_connected():
                conn.close()

    def get_dashboard_metrics(self):
        """Get summary metrics for the dashboard.
        
        Returns:
            dict: Dashboard metrics with keys: total, phishing, scam, safe
        """
        conn = None
        try:
            conn = self._get_connection()
            cursor = conn.cursor(dictionary=True)

            # Total scans
            cursor.execute("SELECT COUNT(*) AS count FROM scan_records")
            total = cursor.fetchone()['count']

            # Phishing detections (URL scans classified as Phishing)
            cursor.execute(
                "SELECT COUNT(*) AS count FROM scan_records WHERE prediction = %s",
                ('Phishing',)
            )
            phishing = cursor.fetchone()['count']

            # Scam detections (Message scans classified as Scam)
            cursor.execute(
                "SELECT COUNT(*) AS count FROM scan_records WHERE prediction = %s",
                ('Scam',)
            )
            scam = cursor.fetchone()['count']

            # Safe detections
            cursor.execute(
                "SELECT COUNT(*) AS count FROM scan_records WHERE prediction = %s",
                ('Safe',)
            )
            safe = cursor.fetchone()['count']

            cursor.close()
            return {
                'total': total,
                'phishing': phishing,
                'scam': scam,
                'safe': safe
            }

        except Error as e:
            print(f"[DB] Error getting metrics: {e}")
            return {'total': 0, 'phishing': 0, 'scam': 0, 'safe': 0}

        finally:
            if conn and conn.is_connected():
                conn.close()
