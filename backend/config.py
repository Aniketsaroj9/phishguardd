"""PhishGuard Configuration"""

import os

# MySQL Database Configuration
# Falls back to XAMPP-friendly local defaults when env vars aren't set,
# so local development still works without any setup.
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'port': int(os.environ.get('DB_PORT', 3306)),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', ''),
    'database': os.environ.get('DB_NAME', 'phishguard_db'),
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_general_ci'
}

# Flask Configuration
FLASK_CONFIG = {
    'DEBUG': os.environ.get('FLASK_DEBUG', 'false').lower() == 'true',
    'HOST': os.environ.get('HOST', '0.0.0.0'),
    'PORT': int(os.environ.get('PORT', 5000))
}

# CORS Configuration
# In production, set CORS_ORIGINS env var to a comma-separated list of
# allowed frontend URLs, e.g. "https://your-frontend.netlify.app"
_default_origins = 'http://localhost,http://localhost:80,http://localhost:8080,http://127.0.0.1'
CORS_ORIGINS = [
    origin.strip()
    for origin in os.environ.get('CORS_ORIGINS', _default_origins).split(',')
    if origin.strip()
]

# ML Model Paths
ML_CONFIG = {
    'MODEL_PATH': 'ml/model.pkl',
    'VECTORIZER_PATH': 'ml/vectorizer.pkl'
}
