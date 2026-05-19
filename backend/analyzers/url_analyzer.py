"""PhishGuard URL Analyzer

Rule-based heuristic URL analysis engine.
Extracts URL features, applies weighted scoring rules,
classifies as Safe/Suspicious/Phishing, and generates
human-readable explanations for each triggered rule.
"""

import re
from urllib.parse import urlparse


# ========================
# Suspicious Indicators
# ========================

SUSPICIOUS_KEYWORDS = [
    'login', 'signin', 'verify', 'account', 'update', 'secure',
    'banking', 'confirm', 'password', 'credential', 'suspend',
    'authenticate', 'wallet', 'paypal', 'ebay', 'amazon',
    'apple', 'microsoft', 'google', 'netflix', 'facebook'
]

SUSPICIOUS_TLDS = [
    '.xyz', '.top', '.club', '.work', '.click', '.link',
    '.info', '.tk', '.ml', '.ga', '.cf', '.gq', '.buzz',
    '.icu', '.cam', '.rest', '.monster'
]

SHORTENER_DOMAINS = [
    'bit.ly', 'tinyurl.com', 't.co', 'goo.gl', 'is.gd',
    'buff.ly', 'ow.ly', 'rebrand.ly', 'short.io'
]


# ========================
# Feature Extraction
# ========================

def extract_features(url):
    """Extract all analyzable features from a URL.
    
    Args:
        url: URL string to analyze
    
    Returns:
        dict: Extracted URL features
    """
    # Ensure URL has a scheme for proper parsing
    parsed_url = url
    if not url.startswith(('http://', 'https://')):
        parsed_url = 'http://' + url
    
    parsed = urlparse(parsed_url)
    
    domain = parsed.netloc.lower()
    path = parsed.path.lower()
    full_url = url.lower()
    
    features = {
        'url': url,
        'scheme': parsed.scheme,
        'domain': domain,
        'path': path,
        'url_length': len(url),
        'domain_length': len(domain),
        'path_length': len(path),
        'dot_count': full_url.count('.'),
        'hyphen_count': full_url.count('-'),
        'at_sign': '@' in url,
        'double_slash_redirect': url.count('//') > 1,
        'has_ip': bool(re.match(r'^https?://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', parsed_url)),
        'has_https': parsed.scheme == 'https',
        'has_subdomain': domain.count('.') > 1,
        'subdomain_count': max(0, domain.count('.') - 1),
        'suspicious_keywords': [],
        'suspicious_tld': False,
        'is_shortener': False,
        'has_query_params': bool(parsed.query),
        'query_length': len(parsed.query),
        'fragment': bool(parsed.fragment),
        'special_char_count': len(re.findall(r'[!@#$%^&*()_+=\[\]{}|;:,<>?]', url))
    }
    
    # Check for suspicious keywords
    for keyword in SUSPICIOUS_KEYWORDS:
        if keyword in full_url:
            features['suspicious_keywords'].append(keyword)
    
    # Check for suspicious TLD
    for tld in SUSPICIOUS_TLDS:
        if domain.endswith(tld):
            features['suspicious_tld'] = True
            break
    
    # Check for URL shorteners
    for shortener in SHORTENER_DOMAINS:
        if shortener in domain:
            features['is_shortener'] = True
            break
    
    return features


# ========================
# Heuristic Scoring
# ========================

def analyze(url):
    """Analyze a URL for phishing indicators using weighted heuristic rules.
    
    Args:
        url: URL string to analyze
    
    Returns:
        dict: Analysis result with keys:
            - url: Original URL
            - risk_score: Numeric score (0-100)
            - classification: 'Safe', 'Suspicious', or 'Phishing'
            - threat_level: Same as classification
            - reasons: List of human-readable explanation strings
            - features: Extracted URL features dict
    """
    features = extract_features(url)
    score = 0
    reasons = []
    
    # Rule 1: HTTP vs HTTPS (weight: 15)
    if not features['has_https']:
        score += 15
        reasons.append("Uses insecure HTTP protocol instead of HTTPS")
    
    # Rule 2: IP-based URL (weight: 25)
    if features['has_ip']:
        score += 25
        reasons.append("Uses IP address instead of domain name — common phishing technique")
    
    # Rule 3: URL length (weight: 10-15)
    if features['url_length'] > 100:
        score += 15
        reasons.append(f"Unusually long URL ({features['url_length']} characters) — may hide suspicious content")
    elif features['url_length'] > 75:
        score += 10
        reasons.append(f"Long URL ({features['url_length']} characters)")
    
    # Rule 4: Excessive dots (weight: 10)
    if features['dot_count'] > 4:
        score += 10
        reasons.append(f"Excessive dots in URL ({features['dot_count']}) — may indicate subdomain abuse")
    
    # Rule 5: Hyphens in domain (weight: 10)
    if features['hyphen_count'] > 2:
        score += 10
        reasons.append(f"Multiple hyphens ({features['hyphen_count']}) — common in spoofed domains")
    
    # Rule 6: @ symbol (weight: 20)
    if features['at_sign']:
        score += 20
        reasons.append("Contains @ symbol — can be used to redirect to a different destination")
    
    # Rule 7: Double slash redirect (weight: 15)
    if features['double_slash_redirect']:
        score += 15
        reasons.append("Contains multiple double slashes — may redirect to a malicious site")
    
    # Rule 8: Suspicious keywords (weight: 5 each, max 20)
    keyword_score = min(len(features['suspicious_keywords']) * 5, 20)
    if keyword_score > 0:
        keywords_str = ', '.join(features['suspicious_keywords'][:4])
        score += keyword_score
        reasons.append(f"Contains suspicious keywords: {keywords_str}")
    
    # Rule 9: Suspicious TLD (weight: 15)
    if features['suspicious_tld']:
        score += 15
        reasons.append(f"Uses a suspicious top-level domain commonly associated with phishing")
    
    # Rule 10: URL shortener (weight: 10)
    if features['is_shortener']:
        score += 10
        reasons.append("Uses a URL shortener — hides the true destination")
    
    # Rule 11: Subdomain abuse (weight: 10)
    if features['subdomain_count'] > 2:
        score += 10
        reasons.append(f"Excessive subdomains ({features['subdomain_count']}) — may be impersonating a legitimate site")
    
    # Rule 12: Special characters (weight: 5)
    if features['special_char_count'] > 3:
        score += 5
        reasons.append(f"Contains unusual special characters ({features['special_char_count']})")
    
    # Cap score at 100
    score = min(score, 100)
    
    # Classify based on score thresholds
    if score < 30:
        classification = 'Safe'
    elif score <= 70:
        classification = 'Suspicious'
    else:
        classification = 'Phishing'
    
    # If no reasons found, add a safe message
    if not reasons:
        reasons.append("No suspicious indicators detected")
    
    return {
        'url': url,
        'risk_score': score,
        'classification': classification,
        'threat_level': classification,
        'reasons': reasons,
        'features': features
    }
