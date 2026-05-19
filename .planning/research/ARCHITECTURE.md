# Architecture Research

**Domain:** Phishing URL & Scam Message Detection
**Researched:** 2026-05-19
**Confidence:** HIGH

## Standard Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                        │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌──────────┐│
│  │ Dashboard │  │URL Scanner│  │Msg Scanner│  │ History  ││
│  └─────┬─────┘  └─────┬─────┘  └─────┬─────┘  └────┬─────┘│
│        │              │              │              │       │
├────────┴──────────────┴──────────────┴──────────────┴───────┤
│                    APPLICATION LAYER (Flask API)             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ URL Analyzer │  │ Msg Classifier│  │ Explainer    │      │
│  │ (Heuristic)  │  │ (TF-IDF+LR)  │  │ (Rule-based) │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
│         │                 │                 │               │
├─────────┴─────────────────┴─────────────────┴───────────────┤
│                    DATA LAYER (MySQL)                        │
│  ┌──────────────┐  ┌──────────────┐                         │
│  │ scan_records │  │threat_reasons│                         │
│  └──────────────┘  └──────────────┘                         │
└─────────────────────────────────────────────────────────────┘
```

### Component Responsibilities

| Component | Responsibility | Typical Implementation |
|-----------|----------------|------------------------|
| Dashboard UI | Display metrics, navigation, scan forms | HTML/CSS/Bootstrap + vanilla JS, fetch API calls |
| URL Scanner UI | URL input form, result display with explanations | Bootstrap card with form, result panel, threat indicators |
| Message Scanner UI | Text input for SMS/email, classification result | Bootstrap textarea form, result panel |
| History UI | List past scans, drill-down to details | Bootstrap table with pagination, detail modal |
| Flask API | REST endpoints, request routing, validation | Flask routes with JSON responses |
| URL Analyzer | Heuristic rule-based URL threat scoring | Python module: extract features → apply weighted rules → score |
| Message Classifier | ML-based scam/spam classification | Loaded scikit-learn pipeline (TF-IDF + LogisticRegression) |
| Explainability Engine | Generate human-readable reasons | Rule-based reason mapping from detected indicators |
| MySQL Database | Persistent storage for scans and reasons | Two tables: scan_records + threat_reasons |

## Recommended Project Structure

```
phisingguard/
├── backend/
│   ├── app.py                  # Flask app entry point, route definitions
│   ├── config.py               # DB config, app settings
│   ├── requirements.txt        # Python dependencies
│   ├── analyzers/
│   │   ├── __init__.py
│   │   ├── url_analyzer.py     # URL heuristic scoring engine
│   │   ├── message_analyzer.py # ML message classification
│   │   └── explainer.py        # Explanation generation
│   ├── models/
│   │   ├── __init__.py
│   │   ├── database.py         # MySQL connection & queries
│   │   └── schemas.py          # Request/response validation
│   ├── ml/
│   │   ├── train_model.py      # Training script (run once)
│   │   ├── model.pkl           # Serialized trained model
│   │   ├── vectorizer.pkl      # Serialized TF-IDF vectorizer
│   │   └── dataset/            # Training data (SMS Spam Collection)
│   └── utils/
│       └── helpers.py          # Shared utility functions
├── frontend/
│   ├── index.html              # Main dashboard page
│   ├── css/
│   │   └── style.css           # Custom styles (extends Bootstrap)
│   ├── js/
│   │   ├── app.js              # Main application logic
│   │   ├── url-scanner.js      # URL scanning module
│   │   ├── msg-scanner.js      # Message scanning module
│   │   ├── history.js          # History display module
│   │   └── dashboard.js        # Dashboard metrics module
│   └── assets/
│       └── images/             # Icons, logos
├── database/
│   └── schema.sql              # MySQL schema creation script
├── .planning/                  # GSD planning documents
└── README.md
```

### Structure Rationale

- **backend/analyzers/:** Separates analysis logic from routing — each analyzer is independently testable
- **backend/ml/:** Isolates ML artifacts (model, vectorizer, training data) from app code
- **backend/models/:** Database access layer — all SQL queries centralized here
- **frontend/js/:** Module-per-feature pattern — each UI section has its own JS file
- **database/:** Schema versioning — SQL files can be committed and replayed

## Architectural Patterns

### Pattern 1: Pipeline Pattern (ML Classification)

**What:** Chain preprocessing → feature extraction → classification into a scikit-learn Pipeline
**When to use:** Any ML inference endpoint
**Trade-offs:** Simple to serialize/load; harder to debug individual steps

**Example:**
```python
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words='english', ngram_range=(1, 2))),
    ('classifier', LogisticRegression(max_iter=1000))
])
pipeline.fit(X_train, y_train)
```

### Pattern 2: Weighted Heuristic Scoring (URL Analysis)

**What:** Assign numeric weights to URL features, sum for composite risk score
**When to use:** Rule-based threat assessment where features have different importance
**Trade-offs:** Transparent and explainable; requires manual weight tuning; brittle against novel attacks

**Example:**
```python
def analyze_url(url):
    score = 0
    reasons = []
    if 'http://' in url:
        score += 15
        reasons.append("Uses insecure HTTP protocol")
    if len(url) > 75:
        score += 10
        reasons.append(f"Unusually long URL ({len(url)} characters)")
    if url.count('.') > 4:
        score += 10
        reasons.append(f"Excessive dots in URL ({url.count('.')})")
    return score, reasons
```

### Pattern 3: Service Layer Pattern (API Routes)

**What:** Thin route handlers that delegate to service/analyzer modules
**When to use:** All Flask routes
**Trade-offs:** Clean separation of concerns; slightly more files

**Example:**
```python
@app.route('/api/analyze-url', methods=['POST'])
def analyze_url_route():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({"error": "URL is required"}), 400
    result = url_analyzer.analyze(url)
    db.save_scan(result)
    return jsonify(result)
```

## Data Flow

### URL Analysis Flow

```
[User submits URL]
    ↓
[Flask /api/analyze-url] → [Validate URL format]
    ↓
[URL Analyzer] → [Extract features: length, dots, protocol, keywords, TLD...]
    ↓
[Apply weighted heuristic rules] → [Calculate risk score 0-100]
    ↓
[Classify: Safe (<30) / Suspicious (30-70) / Phishing (>70)]
    ↓
[Explainability Engine] → [Map triggered rules to human reasons]
    ↓
[Save to MySQL (scan_records + threat_reasons)]
    ↓
[Return JSON response to frontend]
```

### Message Analysis Flow

```
[User submits message text]
    ↓
[Flask /api/analyze-message] → [Validate input]
    ↓
[Load serialized pipeline (TF-IDF + LR)]
    ↓
[Preprocess: lowercase, remove punctuation, tokenize]
    ↓
[TF-IDF vectorize] → [Logistic Regression predict + predict_proba]
    ↓
[Classify: Safe / Scam] + [Confidence score]
    ↓
[Explainability Engine] → [Keyword-based reason generation]
    ↓
[Save to MySQL] → [Return JSON response]
```

## Anti-Patterns

### Anti-Pattern 1: Training ML Model on Every Request

**What people do:** Load training data and retrain model per API call
**Why it's wrong:** Extremely slow (seconds per request); wastes resources
**Do this instead:** Train once, serialize with joblib, load at app startup

### Anti-Pattern 2: Hardcoding Database Credentials

**What people do:** Put MySQL password directly in app.py
**Why it's wrong:** Security risk; can't change without code modification
**Do this instead:** Use config.py or environment variables

### Anti-Pattern 3: Monolithic Route File

**What people do:** Put all logic (parsing, analysis, DB queries, response) in route handlers
**Why it's wrong:** Untestable, unmaintainable, hard to debug
**Do this instead:** Thin routes that delegate to analyzer modules and database layer

## Integration Points

### Internal Boundaries

| Boundary | Communication | Notes |
|----------|---------------|-------|
| Frontend ↔ Flask API | REST/JSON over HTTP | CORS required; fetch() from JS |
| Flask API ↔ URL Analyzer | Direct Python import | Same process, no network overhead |
| Flask API ↔ ML Model | joblib.load() at startup | Model loaded once, reused for all requests |
| Flask API ↔ MySQL | mysql-connector-python | Connection pooling recommended for concurrent requests |

## Sources

- Web research: phishing detection system architecture Flask MySQL
- Web research: explainable AI cybersecurity web application patterns
- scikit-learn Pipeline documentation
- Flask REST API best practices

---
*Architecture research for: Phishing URL & Scam Message Detection*
*Researched: 2026-05-19*
