---
phase: 1
plan: 01
title: "MySQL Database Schema & Connection Layer"
wave: 1
depends_on: []
files_modified:
  - backend/config.py
  - backend/models/database.py
  - database/schema.sql
requirements:
  - DB-01
  - DB-02
  - DB-03
autonomous: true
---

# Plan 01: MySQL Database Schema & Connection Layer

<objective>
Create the MySQL database schema for PhishGuard and the Python database connection layer with auto-creation capability. This establishes the data foundation that all subsequent phases depend on.
</objective>

<must_haves>
- MySQL database `phishguard_db` created with correct tables
- `scan_records` table with all required columns
- `threat_reasons` table with foreign key to scan_records
- Auto-create database and tables on app startup
- All queries use parameterized statements
- Connection configuration in config.py with XAMPP defaults
</must_haves>

## Tasks

<task id="01.1" title="Create project directory structure">
<read_first>
- .planning/research/ARCHITECTURE.md (project structure section)
- .planning/phases/01-database-backend-foundation/01-CONTEXT.md (D-04, D-05, D-06)
</read_first>

<action>
Create the full project directory structure:

```
phisingguard/
├── backend/
│   ├── app.py                  # (created in Plan 02)
│   ├── config.py               # Database and app configuration
│   ├── requirements.txt        # Python dependencies
│   ├── analyzers/
│   │   ├── __init__.py
│   │   ├── url_analyzer.py     # (placeholder for Phase 3)
│   │   ├── message_analyzer.py # (placeholder for Phase 4)
│   │   └── explainer.py        # (placeholder for Phase 3/4)
│   ├── models/
│   │   ├── __init__.py
│   │   └── database.py         # MySQL connection & queries
│   ├── ml/
│   │   └── .gitkeep            # (populated in Phase 2)
│   └── utils/
│       ├── __init__.py
│       └── helpers.py          # Shared utility functions
├── frontend/
│   ├── index.html              # (populated in Phase 5)
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── app.js
│   └── assets/
│       └── .gitkeep
├── database/
│   └── schema.sql              # MySQL schema creation script
└── .planning/                  # Already exists
```

Create all directories and placeholder __init__.py files. Each __init__.py should be empty.
</action>

<acceptance_criteria>
- `backend/config.py` file exists
- `backend/models/__init__.py` file exists
- `backend/models/database.py` file exists
- `backend/analyzers/__init__.py` file exists
- `backend/ml/` directory exists
- `database/schema.sql` file exists
- `frontend/index.html` file exists
- `backend/requirements.txt` file exists
</acceptance_criteria>
</task>

<task id="01.2" title="Create config.py with XAMPP defaults">
<read_first>
- .planning/phases/01-database-backend-foundation/01-CONTEXT.md (D-01, D-09)
</read_first>

<action>
Create `backend/config.py` with the following exact content:

```python
"""PhishGuard Configuration"""

# MySQL Database Configuration (XAMPP defaults)
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'phishguard_db',
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_general_ci'
}

# Flask Configuration
FLASK_CONFIG = {
    'DEBUG': True,
    'HOST': '0.0.0.0',
    'PORT': 5000
}

# CORS Configuration
CORS_ORIGINS = [
    'http://localhost',
    'http://localhost:80',
    'http://localhost:8080',
    'http://127.0.0.1'
]

# ML Model Paths
ML_CONFIG = {
    'MODEL_PATH': 'ml/model.pkl',
    'VECTORIZER_PATH': 'ml/vectorizer.pkl'
}
```
</action>

<acceptance_criteria>
- `backend/config.py` contains `DB_CONFIG`
- `backend/config.py` contains `'host': 'localhost'`
- `backend/config.py` contains `'user': 'root'`
- `backend/config.py` contains `'password': ''`
- `backend/config.py` contains `'database': 'phishguard_db'`
- `backend/config.py` contains `CORS_ORIGINS`
- `backend/config.py` contains `'http://localhost'`
- `backend/config.py` contains `ML_CONFIG`
</acceptance_criteria>
</task>

<task id="01.3" title="Create SQL schema file">
<read_first>
- .planning/REQUIREMENTS.md (DB-01, DB-02)
- .planning/phases/01-database-backend-foundation/01-CONTEXT.md (D-02)
</read_first>

<action>
Create `database/schema.sql` with the exact schema:

```sql
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
```
</action>

<acceptance_criteria>
- `database/schema.sql` contains `CREATE DATABASE IF NOT EXISTS phishguard_db`
- `database/schema.sql` contains `CREATE TABLE IF NOT EXISTS scan_records`
- `database/schema.sql` contains `scan_id INT AUTO_INCREMENT PRIMARY KEY`
- `database/schema.sql` contains `scan_type ENUM('URL', 'SMS', 'Email')`
- `database/schema.sql` contains `CREATE TABLE IF NOT EXISTS threat_reasons`
- `database/schema.sql` contains `FOREIGN KEY (scan_id) REFERENCES scan_records(scan_id)`
- `database/schema.sql` contains `ON DELETE CASCADE`
</acceptance_criteria>
</task>

<task id="01.4" title="Create database.py connection layer with auto-create">
<read_first>
- backend/config.py (for DB_CONFIG import)
- database/schema.sql (for table structure reference)
- .planning/phases/01-database-backend-foundation/01-CONTEXT.md (D-02, D-03)
- .planning/research/PITFALLS.md (SQL injection prevention section)
</read_first>

<action>
Create `backend/models/database.py` with a Database class that:

1. **Connects to MySQL** using mysql-connector-python with config from config.py
2. **Auto-creates database and tables** on initialization if they don't exist
3. **Provides parameterized query methods** for:
   - `save_scan(scan_type, content, prediction, risk_score, threat_level, reasons)` → returns scan_id
   - `get_scan(scan_id)` → returns scan record with threat reasons
   - `get_history(limit=50, offset=0)` → returns paginated scan records
   - `get_dashboard_metrics()` → returns counts (total, phishing, scam, safe)
4. **Uses context manager** for connection handling
5. **All queries MUST use parameterized statements** (cursor.execute with %s placeholders)
6. **No string concatenation in any SQL query**

Key implementation details:
- First connect WITHOUT database name to create the database
- Then reconnect WITH database name to create tables
- Use `cursor.execute("CREATE DATABASE IF NOT EXISTS %s" ...)` is NOT valid — database names cannot be parameterized. Use the exact string from config: `cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']} ...")`
- All user-input queries (save, get) MUST use `cursor.execute(query, (param1, param2))` parameterized form
- `get_dashboard_metrics()` should return: `{'total': N, 'phishing': N, 'scam': N, 'safe': N}`
- `save_scan()` should insert into scan_records AND threat_reasons in a single transaction
</action>

<acceptance_criteria>
- `backend/models/database.py` contains `import mysql.connector`
- `backend/models/database.py` contains `from config import DB_CONFIG`
- `backend/models/database.py` contains `CREATE DATABASE IF NOT EXISTS`
- `backend/models/database.py` contains `CREATE TABLE IF NOT EXISTS scan_records`
- `backend/models/database.py` contains `CREATE TABLE IF NOT EXISTS threat_reasons`
- `backend/models/database.py` contains `def save_scan(`
- `backend/models/database.py` contains `def get_scan(`
- `backend/models/database.py` contains `def get_history(`
- `backend/models/database.py` contains `def get_dashboard_metrics(`
- `backend/models/database.py` does NOT contain string concatenation in SQL (no `"SELECT" + variable` or `f"SELECT...{user_input}"` patterns in query execution — database name in CREATE DATABASE is the only exception)
- `backend/models/database.py` contains `cursor.execute(` with parameterized queries using `%s`
</acceptance_criteria>
</task>

<task id="01.5" title="Create requirements.txt">
<read_first>
- .planning/research/STACK.md (installation section)
</read_first>

<action>
Create `backend/requirements.txt` with exact content:

```
flask==3.1.1
flask-cors==5.0.1
mysql-connector-python==9.2.0
scikit-learn==1.6.1
pandas==2.2.3
nltk==3.9.1
joblib==1.4.2
```
</action>

<acceptance_criteria>
- `backend/requirements.txt` contains `flask==`
- `backend/requirements.txt` contains `flask-cors==`
- `backend/requirements.txt` contains `mysql-connector-python==`
- `backend/requirements.txt` contains `scikit-learn==`
- `backend/requirements.txt` contains `pandas==`
- `backend/requirements.txt` contains `nltk==`
- `backend/requirements.txt` contains `joblib==`
</acceptance_criteria>
</task>

<verification>
After all tasks complete:
1. `backend/config.py` exists with DB_CONFIG and CORS_ORIGINS
2. `database/schema.sql` has valid SQL for both tables with foreign key
3. `backend/models/database.py` has all 4 query methods with parameterized statements
4. `backend/requirements.txt` lists all dependencies
5. Zero string concatenation in SQL queries (except database name in CREATE DATABASE)
</verification>
