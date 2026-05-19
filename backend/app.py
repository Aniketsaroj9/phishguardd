"""PhishGuard - AI-Powered Phishing URL & Scam Detection System

Main Flask application entry point.
Configures CORS, initializes database, and defines all API routes.
"""

import sys
import os

# Add backend directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request
from flask_cors import CORS
from config import FLASK_CONFIG, CORS_ORIGINS
from models.database import Database
from utils.helpers import success_response, error_response

# Initialize Flask app
app = Flask(__name__)

# Configure CORS - restricted to localhost only
CORS(app, origins=CORS_ORIGINS)

# Initialize database (auto-creates DB and tables)
db = Database()


# ========================
# Health Check Endpoint
# ========================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Check backend health status."""
    return success_response({
        'status': 'ok',
        'service': 'PhishGuard API',
        'version': '1.0.0'
    })


# ========================
# Error Handlers
# ========================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors with JSON response."""
    return error_response('Endpoint not found', 404)


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors with JSON response."""
    return error_response('Method not allowed', 405)


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors with JSON response."""
    return error_response('Internal server error', 500)


# ========================
# URL Analysis (Phase 3)
# ========================

@app.route('/api/analyze-url', methods=['POST'])
def analyze_url():
    """Analyze a suspicious URL for phishing indicators."""
    return error_response('URL analysis not yet implemented', 501)


# ========================
# Message Analysis (Phase 4)
# ========================

@app.route('/api/analyze-message', methods=['POST'])
def analyze_message():
    """Analyze a suspicious SMS/email message for scam indicators."""
    return error_response('Message analysis not yet implemented', 501)


# ========================
# Scan History (Phase 4)
# ========================

@app.route('/api/history', methods=['GET'])
def get_history():
    """Get paginated scan history."""
    return error_response('History not yet implemented', 501)


@app.route('/api/history/<int:scan_id>', methods=['GET'])
def get_scan_detail(scan_id):
    """Get detailed scan record with threat reasons."""
    return error_response('Scan detail not yet implemented', 501)


# ========================
# Dashboard Metrics (Phase 4)
# ========================

@app.route('/api/dashboard-metrics', methods=['GET'])
def get_dashboard_metrics():
    """Get dashboard summary metrics."""
    return error_response('Dashboard metrics not yet implemented', 501)


# ========================
# Run Application
# ========================

if __name__ == '__main__':
    print("=" * 50)
    print("  PhishGuard API Server")
    print("  http://localhost:5000")
    print("=" * 50)
    app.run(
        debug=FLASK_CONFIG['DEBUG'],
        host=FLASK_CONFIG['HOST'],
        port=FLASK_CONFIG['PORT']
    )
