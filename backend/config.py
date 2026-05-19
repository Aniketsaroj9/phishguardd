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
