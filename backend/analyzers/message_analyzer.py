"""PhishGuard Message Analyzer

ML-based message classification using trained TF-IDF + Logistic Regression model.
Classifies SMS/email text as Safe or Scam with confidence score
and generates human-readable explanations.
"""

import os
import re
import joblib


# ========================
# Configuration
# ========================

MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ml', 'model.pkl')
VECTORIZER_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ml', 'vectorizer.pkl')

# Scam indicator keywords for explanation generation
SCAM_INDICATORS = {
    'urgency': ['urgent', 'immediately', 'act now', 'hurry', 'expire', 'limited time',
                'last chance', 'don\'t miss', 'deadline', 'asap', 'right away'],
    'financial': ['win', 'won', 'prize', 'cash', 'money', 'bank', 'credit',
                  'loan', 'investment', 'free', 'offer', 'discount', 'jackpot'],
    'action': ['click', 'call', 'reply', 'text', 'send', 'visit', 'confirm',
               'verify', 'update', 'claim', 'subscribe', 'register'],
    'threat': ['suspend', 'block', 'unauthorized', 'locked', 'compromised',
               'unusual activity', 'security alert', 'violation', 'penalty'],
    'identity': ['password', 'otp', 'pin', 'ssn', 'account number', 'cvv',
                 'social security', 'credentials', 'login', 'verification code']
}


# ========================
# Model Loading
# ========================

_model = None
_vectorizer = None


def _load_model():
    """Load the trained model and vectorizer from disk.
    
    Returns:
        tuple: (model_pipeline, vectorizer) or (None, None) if loading fails
    """
    global _model, _vectorizer
    
    if _model is not None:
        return _model, _vectorizer
    
    try:
        if not os.path.exists(MODEL_PATH):
            print(f"[ML] Model file not found: {MODEL_PATH}")
            print("[ML] Run 'python ml/train_model.py' to train the model first.")
            return None, None
        
        _model = joblib.load(MODEL_PATH)
        _vectorizer = joblib.load(VECTORIZER_PATH)
        print("[ML] Model loaded successfully.")
        return _model, _vectorizer
    
    except Exception as e:
        print(f"[ML] Error loading model: {e}")
        return None, None


# ========================
# Text Preprocessing
# ========================

def preprocess_text(text):
    """Clean and preprocess message text (same as training pipeline).
    
    Args:
        text: Raw message string
    
    Returns:
        Cleaned lowercase text with punctuation removed
    """
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


# ========================
# Explanation Generation
# ========================

def _generate_reasons(text, prediction, confidence):
    """Generate human-readable explanations for the classification.
    
    Args:
        text: Original message text (lowercase)
        prediction: 0 (Safe) or 1 (Scam)
        confidence: Prediction probability
    
    Returns:
        list: Human-readable reason strings
    """
    reasons = []
    text_lower = text.lower()
    
    if prediction == 0:  # Safe
        reasons.append("No significant scam indicators detected in the message")
        if confidence > 0.9:
            reasons.append("High confidence in safe classification")
        return reasons
    
    # Scam detected — find which indicator categories match
    matched_categories = {}
    for category, keywords in SCAM_INDICATORS.items():
        matched = [kw for kw in keywords if kw in text_lower]
        if matched:
            matched_categories[category] = matched
    
    # Generate category-specific reasons
    if 'urgency' in matched_categories:
        keywords_str = ', '.join(matched_categories['urgency'][:3])
        reasons.append(f"Contains urgency language: {keywords_str}")
    
    if 'financial' in matched_categories:
        keywords_str = ', '.join(matched_categories['financial'][:3])
        reasons.append(f"Financial scam indicators detected: {keywords_str}")
    
    if 'action' in matched_categories:
        keywords_str = ', '.join(matched_categories['action'][:3])
        reasons.append(f"Prompts suspicious action: {keywords_str}")
    
    if 'threat' in matched_categories:
        keywords_str = ', '.join(matched_categories['threat'][:3])
        reasons.append(f"Contains threatening language: {keywords_str}")
    
    if 'identity' in matched_categories:
        keywords_str = ', '.join(matched_categories['identity'][:3])
        reasons.append(f"Requests sensitive personal information: {keywords_str}")
    
    # If ML flagged it but no keyword matches, give generic reason
    if not reasons:
        reasons.append("Message pattern matches known scam templates")
    
    # Add confidence note
    if confidence > 0.9:
        reasons.append(f"High confidence scam detection ({confidence*100:.0f}%)")
    elif confidence > 0.7:
        reasons.append(f"Moderate confidence scam detection ({confidence*100:.0f}%)")
    
    return reasons


# ========================
# Main Analysis
# ========================

def analyze(content, message_type='SMS'):
    """Analyze a message for scam indicators using ML classification.
    
    Args:
        content: Message text to analyze
        message_type: 'SMS' or 'Email' (stored for record-keeping)
    
    Returns:
        dict: Analysis result with keys:
            - content: Original message (truncated for display)
            - message_type: SMS or Email
            - classification: 'Safe' or 'Scam'
            - threat_level: Same as classification
            - confidence: Prediction probability (0.0-1.0)
            - risk_score: Confidence mapped to 0-100 scale
            - reasons: List of human-readable explanation strings
    """
    model, vectorizer = _load_model()
    
    if model is None:
        return {
            'content': content[:100],
            'message_type': message_type,
            'classification': 'Unknown',
            'threat_level': 'Unknown',
            'confidence': 0.0,
            'risk_score': 0.0,
            'reasons': ['ML model not available. Run train_model.py first.'],
            'error': True
        }
    
    # Preprocess
    cleaned = preprocess_text(content)
    
    # Predict using the pipeline (includes TF-IDF + LR)
    prediction = model.predict([cleaned])[0]
    probabilities = model.predict_proba([cleaned])[0]
    
    # Get confidence for the predicted class
    confidence = probabilities[prediction]
    
    # Calculate risk score (scam probability * 100)
    scam_probability = probabilities[1]  # Probability of being scam
    risk_score = scam_probability * 100
    
    # HYBRID SCORING: Boost risk score based on known scam keywords
    # (Helps catch zero-day phishing that the ML model hasn't seen)
    text_lower = content.lower()
    keyword_boost = 0
    matched_categories = {}
    
    for category, keywords in SCAM_INDICATORS.items():
        matched = [kw for kw in keywords if kw in text_lower]
        if matched:
            matched_categories[category] = matched
            # Boost score: +15 for hitting a category, +5 for each specific word
            keyword_boost += 15 + (len(matched) * 5)
            
    risk_score += keyword_boost
    risk_score = min(risk_score, 100.0)  # Cap at 100
    
    # Recalculate classification based on hybrid score
    if risk_score >= 50.0:
        classification = 'Scam'
        prediction = 1  # Override prediction for explanation generator
        
        # Override confidence to match the boosted risk score
        confidence = risk_score / 100.0
    else:
        classification = 'Safe'
        prediction = 0
    
    risk_score = round(risk_score, 1)
    
    # Generate explanations
    reasons = _generate_reasons(content, prediction, confidence)
    
    return {
        'content': content[:200],
        'message_type': message_type,
        'classification': classification,
        'threat_level': classification,
        'confidence': round(confidence, 4),
        'risk_score': risk_score,
        'reasons': reasons
    }
