---
phase: 1
plan: 02
title: "Flask Application Skeleton & API Infrastructure"
wave: 2
depends_on: [01]
files_modified:
  - backend/app.py
  - backend/utils/helpers.py
requirements:
  - API-06
  - API-07
autonomous: true
---

# Plan 02: Flask Application Skeleton & API Infrastructure

<objective>
Create the Flask application entry point with CORS configuration, health endpoint, consistent error handling, and JSON response utilities. This establishes the API infrastructure that Phases 3-5 build on.
</objective>

<must_haves>
- Flask app starts successfully with debug mode
- CORS configured for localhost origins only
- GET /api/health returns {"success": true, "data": {"status": "ok"}}
- All error responses use consistent JSON format
- Database initializes on app startup (auto-create)
</must_haves>

## Tasks

<task id="02.1" title="Create helpers.py with response utilities">
<read_first>
- .planning/phases/01-database-backend-foundation/01-CONTEXT.md (D-07)
</read_first>

<action>
Create `backend/utils/helpers.py` with response helper functions:

```python
"""PhishGuard Utility Helpers"""

from flask import jsonify


def success_response(data, status_code=200):
    """Create a standardized success response.
    
    Args:
        data: Response data (dict or list)
        status_code: HTTP status code (default 200)
    
    Returns:
        Flask JSON response with format: {"success": true, "data": {...}}
    """
    response = jsonify({
        'success': True,
        'data': data
    })
    response.status_code = status_code
    return response


def error_response(message, status_code=400):
    """Create a standardized error response.
    
    Args:
        message: Error message string
        status_code: HTTP status code (default 400)
    
    Returns:
        Flask JSON response with format: {"success": false, "error": "..."}
    """
    response = jsonify({
        'success': False,
        'error': message
    })
    response.status_code = status_code
    return response


def validate_url(url):
    """Basic URL validation.
    
    Args:
        url: URL string to validate
    
    Returns:
        tuple: (is_valid: bool, error_message: str or None)
    """
    if not url or not isinstance(url, str):
        return False, "URL is required and must be a string"
    
    url = url.strip()
    if len(url) == 0:
        return False, "URL cannot be empty"
    
    if not url.startswith(('http://', 'https://', 'www.')):
        return False, "URL must start with http://, https://, or www."
    
    return True, None


def validate_message(content, message_type=None):
    """Basic message content validation.
    
    Args:
        content: Message text to validate
        message_type: Optional type (SMS/Email)
    
    Returns:
        tuple: (is_valid: bool, error_message: str or None)
    """
    if not content or not isinstance(content, str):
        return False, "Message content is required and must be a string"
    
    content = content.strip()
    if len(content) == 0:
        return False, "Message content cannot be empty"
    
    if message_type and message_type not in ('SMS', 'Email'):
        return False, "Message type must be 'SMS' or 'Email'"
    
    return True, None
```
</action>

<acceptance_criteria>
- `backend/utils/helpers.py` contains `def success_response(`
- `backend/utils/helpers.py` contains `def error_response(`
- `backend/utils/helpers.py` contains `def validate_url(`
- `backend/utils/helpers.py` contains `def validate_message(`
- `backend/utils/helpers.py` contains `'success': True`
- `backend/utils/helpers.py` contains `'success': False`
</acceptance_criteria>
</task>

<task id="02.2" title="Create Flask app.py with health endpoint and error handlers">
<read_first>
- backend/config.py (for FLASK_CONFIG, CORS_ORIGINS)
- backend/models/database.py (for Database class import)
- backend/utils/helpers.py (for response helpers)
- .planning/phases/01-database-backend-foundation/01-CONTEXT.md (D-07, D-08, D-09)
</read_first>

<action>
Create `backend/app.py` as the Flask application entry point:

```python
"""PhishGuard - AI-Powered Phishing URL & Scam Detection System"""

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
# Placeholder Routes (Phases 3-4)
# ========================

@app.route('/api/analyze-url', methods=['POST'])
def analyze_url():
    """Analyze a suspicious URL (implemented in Phase 3)."""
    return error_response('URL analysis not yet implemented', 501)


@app.route('/api/analyze-message', methods=['POST'])
def analyze_message():
    """Analyze a suspicious message (implemented in Phase 4)."""
    return error_response('Message analysis not yet implemented', 501)


@app.route('/api/history', methods=['GET'])
def get_history():
    """Get scan history (implemented in Phase 4)."""
    return error_response('History not yet implemented', 501)


@app.route('/api/history/<int:scan_id>', methods=['GET'])
def get_scan_detail(scan_id):
    """Get detailed scan record (implemented in Phase 4)."""
    return error_response('Scan detail not yet implemented', 501)


@app.route('/api/dashboard-metrics', methods=['GET'])
def get_dashboard_metrics():
    """Get dashboard summary metrics (implemented in Phase 4)."""
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
```

This gives every planned API endpoint a stub that returns a 501 "not yet implemented" response, so the frontend team (Phase 5) can start work knowing the endpoint contract.
</action>

<acceptance_criteria>
- `backend/app.py` contains `from flask import Flask`
- `backend/app.py` contains `from flask_cors import CORS`
- `backend/app.py` contains `CORS(app, origins=CORS_ORIGINS)`
- `backend/app.py` contains `db = Database()`
- `backend/app.py` contains `@app.route('/api/health'`
- `backend/app.py` contains `'status': 'ok'`
- `backend/app.py` contains `@app.errorhandler(404)`
- `backend/app.py` contains `@app.errorhandler(500)`
- `backend/app.py` contains `@app.route('/api/analyze-url'`
- `backend/app.py` contains `@app.route('/api/analyze-message'`
- `backend/app.py` contains `@app.route('/api/history'`
- `backend/app.py` contains `@app.route('/api/dashboard-metrics'`
- `backend/app.py` contains `if __name__ == '__main__':`
- `backend/app.py` contains `app.run(`
</acceptance_criteria>
</task>

<verification>
After all tasks complete:
1. `python backend/app.py` starts Flask server on port 5000 without errors
2. `GET http://localhost:5000/api/health` returns `{"success": true, "data": {"status": "ok", ...}}`
3. `POST http://localhost:5000/api/analyze-url` returns 501 with JSON error
4. `GET http://localhost:5000/nonexistent` returns 404 with JSON error (not HTML)
5. Database `phishguard_db` auto-created with `scan_records` and `threat_reasons` tables
6. CORS headers present in responses (Access-Control-Allow-Origin: http://localhost)
</verification>
