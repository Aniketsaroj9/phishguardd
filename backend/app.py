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
from analyzers import url_analyzer, message_analyzer
from utils.helpers import success_response, error_response, validate_url, validate_message

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
# URL Analysis
# ========================

@app.route('/api/analyze-url', methods=['POST'])
def analyze_url():
    """Analyze a suspicious URL for phishing indicators."""
    data = request.get_json()
    
    if not data:
        return error_response('Request body must be JSON', 400)
    
    url = data.get('url', '').strip()
    
    # Validate
    is_valid, err_msg = validate_url(url)
    if not is_valid:
        return error_response(err_msg, 400)
    
    # Analyze
    result = url_analyzer.analyze(url)
    
    # Save to database
    scan_id = db.save_scan(
        scan_type='URL',
        content=url,
        prediction=result['classification'],
        risk_score=result['risk_score'],
        threat_level=result['threat_level'],
        reasons=result['reasons']
    )
    
    result['scan_id'] = scan_id
    
    # Remove internal features from response
    result.pop('features', None)
    
    return success_response(result)


# ========================
# Message Analysis
# ========================

@app.route('/api/analyze-message', methods=['POST'])
def analyze_message():
    """Analyze a suspicious SMS/email message for scam indicators."""
    data = request.get_json()
    
    if not data:
        return error_response('Request body must be JSON', 400)
    
    content = data.get('content', '').strip()
    message_type = data.get('message_type', 'SMS')
    
    # Validate
    is_valid, err_msg = validate_message(content, message_type)
    if not is_valid:
        return error_response(err_msg, 400)
    
    # Analyze
    result = message_analyzer.analyze(content, message_type)
    
    # Check for model error
    if result.get('error'):
        return error_response(result['reasons'][0], 503)
    
    # Save to database
    scan_id = db.save_scan(
        scan_type=message_type,
        content=content,
        prediction=result['classification'],
        risk_score=result['risk_score'],
        threat_level=result['threat_level'],
        reasons=result['reasons']
    )
    
    result['scan_id'] = scan_id
    
    return success_response(result)


# ========================
# Scan History
# ========================

@app.route('/api/history', methods=['GET'])
def get_history():
    """Get paginated scan history."""
    try:
        limit = int(request.args.get('limit', 50))
        offset = int(request.args.get('offset', 0))
    except ValueError:
        return error_response('limit and offset must be integers', 400)
    
    # Clamp values
    limit = min(max(limit, 1), 100)
    offset = max(offset, 0)
    
    records = db.get_history(limit=limit, offset=offset)
    
    return success_response({
        'records': records,
        'limit': limit,
        'offset': offset,
        'count': len(records)
    })


@app.route('/api/history/<int:scan_id>', methods=['GET'])
def get_scan_detail(scan_id):
    """Get detailed scan record with threat reasons."""
    scan = db.get_scan(scan_id)
    
    if not scan:
        return error_response(f'Scan record {scan_id} not found', 404)
    
    return success_response(scan)


# ========================
# Dashboard Metrics
# ========================

@app.route('/api/dashboard-metrics', methods=['GET'])
def get_dashboard_metrics():
    """Get dashboard summary metrics."""
    metrics = db.get_dashboard_metrics()
    return success_response(metrics)


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
