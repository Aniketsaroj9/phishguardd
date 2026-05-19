"""PhishGuard Utility Helpers

Response formatting utilities and input validation functions.
All API endpoints use these for consistent JSON responses.
"""

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
