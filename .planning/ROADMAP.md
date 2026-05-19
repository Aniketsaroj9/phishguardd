# PhishGuard — Roadmap

## Milestone 1: MVP

### Phase 1: Database & Backend Foundation
**Goal:** Set up MySQL database schema, Flask application skeleton, and core infrastructure
**Requirements:** DB-01, DB-02, DB-03, API-06, API-07
**Depends on:** None
**UI hint:** no

**Success Criteria:**
1. MySQL database `phishguard_db` created with `scan_records` and `threat_reasons` tables
2. Flask app starts successfully with CORS configured
3. GET /api/health returns `{"status": "ok"}` JSON response
4. Database connection uses parameterized queries (zero string concatenation)
5. Error handling returns consistent JSON error responses

---

### Phase 2: ML Model Training & Evaluation
**Goal:** Train, evaluate, and serialize the TF-IDF + Logistic Regression model for message classification
**Requirements:** ML-01, ML-02, ML-03, ML-04, ML-05
**Depends on:** None
**UI hint:** no

**Success Criteria:**
1. SMS Spam Collection Dataset loaded and preprocessed (lowercase, punctuation removal, stopwords)
2. TF-IDF + Logistic Regression pipeline trained with stratified 80/20 split
3. Model achieves 80%+ accuracy, with Precision/Recall/F1 metrics documented
4. Trained model and vectorizer serialized to `.pkl` files in `backend/ml/`
5. Training script is reproducible and committed

---

### Phase 3: URL Analysis Engine + API
**Goal:** Build the rule-based URL heuristic analyzer with explainability and API endpoint
**Requirements:** URL-01, URL-02, URL-03, URL-04, URL-05, URL-06, API-01, PERF-01
**Depends on:** Phase 1
**UI hint:** no

**Success Criteria:**
1. URL feature extraction works for protocol, domain, path length, dots, hyphens, keywords, TLD, IP-based
2. Weighted heuristic scoring produces risk score 0-100
3. Classification maps to Safe/Suspicious/Phishing correctly
4. Human-readable explanations generated for each triggered rule
5. POST /api/analyze-url returns correct JSON with classification, score, reasons
6. Scan results persisted to MySQL (scan_records + threat_reasons)
7. Analysis completes in under 3 seconds

---

### Phase 4: Message Analysis Engine + API
**Goal:** Build the ML-based message classifier with explainability and API endpoints
**Requirements:** MSG-01, MSG-02, MSG-03, MSG-04, MSG-05, MSG-06, API-02, API-03, API-04, API-05, PERF-02
**Depends on:** Phase 1, Phase 2
**UI hint:** no

**Success Criteria:**
1. Message preprocessing pipeline works (lowercase, punctuation, tokenization, stopwords)
2. ML model loaded at startup and classifies messages as Safe/Scam with confidence
3. Human-readable explanations generated for message detections
4. POST /api/analyze-message returns correct JSON with classification, confidence, reasons
5. GET /api/history returns paginated scan records
6. GET /api/history/{id} returns detailed scan with threat reasons
7. GET /api/dashboard-metrics returns correct aggregate counts
8. Message analysis completes in under 5 seconds

---

### Phase 5: Frontend Dashboard & UI
**Goal:** Build the complete frontend with dashboard, scanners, history, and responsive design
**Requirements:** UI-01, UI-02, UI-03, UI-04, UI-05, UI-06, UI-07, UI-08
**Depends on:** Phase 3, Phase 4
**UI hint:** yes

**Success Criteria:**
1. Dashboard displays summary metric cards (total scans, phishing, scam, safe)
2. URL Scanner page accepts URL input, shows loading state, displays color-coded results with explanations
3. Message Scanner page accepts text input, shows loading state, displays classification with explanations
4. History page shows past scans in a table with type, content preview, prediction, score, timestamp
5. Navigation works between all sections (Dashboard, URL Scanner, Message Scanner, History)
6. Design is responsive and works in Chrome, Edge, and Firefox
7. All results show color-coded badges (green=Safe, yellow=Suspicious, red=Phishing/Scam)

---

## Coverage

| Requirement | Phase |
|-------------|-------|
| DB-01 | 1 |
| DB-02 | 1 |
| DB-03 | 1 |
| ML-01 | 2 |
| ML-02 | 2 |
| ML-03 | 2 |
| ML-04 | 2 |
| ML-05 | 2 |
| URL-01 | 3 |
| URL-02 | 3 |
| URL-03 | 3 |
| URL-04 | 3 |
| URL-05 | 3 |
| URL-06 | 3 |
| MSG-01 | 4 |
| MSG-02 | 4 |
| MSG-03 | 4 |
| MSG-04 | 4 |
| MSG-05 | 4 |
| MSG-06 | 4 |
| API-01 | 3 |
| API-02 | 4 |
| API-03 | 4 |
| API-04 | 4 |
| API-05 | 4 |
| API-06 | 1 |
| API-07 | 1 |
| UI-01 | 5 |
| UI-02 | 5 |
| UI-03 | 5 |
| UI-04 | 5 |
| UI-05 | 5 |
| UI-06 | 5 |
| UI-07 | 5 |
| UI-08 | 5 |
| PERF-01 | 3 |
| PERF-02 | 4 |

**Total:** 33 requirements → 5 phases → 100% coverage ✓

---
*Roadmap created: 2026-05-19*
*Milestone: MVP*
