# PhishGuard — v1 Requirements

## v1 Requirements

### Database & Infrastructure

- [ ] **DB-01**: System creates MySQL database `phishguard_db` with `scan_records` table (scan_id, scan_type, submitted_content, prediction, risk_score, threat_level, created_at)
- [ ] **DB-02**: System creates `threat_reasons` table (reason_id, scan_id, reason_text) with foreign key to scan_records
- [ ] **DB-03**: All database queries use parameterized statements (no string concatenation)

### URL Scanning

- [ ] **URL-01**: User can paste a URL into a text field and submit for analysis
- [ ] **URL-02**: System validates URL format before analysis (rejects empty/malformed input with clear error)
- [ ] **URL-03**: System extracts URL features: protocol (HTTP/HTTPS), domain, path length, dot count, hyphen count, suspicious keywords, TLD, IP-based check
- [ ] **URL-04**: System calculates a risk score (0-100) using weighted heuristic rules on extracted features
- [ ] **URL-05**: System classifies URL as Safe (score < 30), Suspicious (30-70), or Phishing (> 70)
- [ ] **URL-06**: System generates human-readable explanations for each triggered detection rule (e.g., "Uses insecure HTTP protocol", "Contains suspicious keyword: login")

### Message Scanning

- [ ] **MSG-01**: User can paste SMS or email text into a textarea and submit for analysis
- [ ] **MSG-02**: System validates message input (rejects empty input with clear error)
- [ ] **MSG-03**: System preprocesses message text (lowercase, remove punctuation, tokenize, remove stopwords)
- [ ] **MSG-04**: System classifies message as Safe or Scam using trained TF-IDF + Logistic Regression model
- [ ] **MSG-05**: System provides confidence score (probability) for the classification
- [ ] **MSG-06**: System generates human-readable explanations for message detections (e.g., "Contains urgency language", "Financial scam indicators detected")

### ML Model

- [ ] **ML-01**: TF-IDF + Logistic Regression pipeline trained on SMS Spam Collection Dataset
- [ ] **ML-02**: Model achieves 80%+ accuracy on stratified test split
- [ ] **ML-03**: Model evaluation includes Precision, Recall, and F1-score metrics
- [ ] **ML-04**: Trained model and vectorizer serialized to .pkl files for production use
- [ ] **ML-05**: Training script is reproducible (documented, committed)

### API Endpoints

- [ ] **API-01**: POST /api/analyze-url accepts JSON `{"url": "..."}` and returns classification, risk score, threat level, explanations
- [ ] **API-02**: POST /api/analyze-message accepts JSON `{"message_type": "SMS|Email", "content": "..."}` and returns classification, confidence, explanations
- [ ] **API-03**: GET /api/history returns list of past scan records with pagination
- [ ] **API-04**: GET /api/history/{id} returns detailed scan record with threat reasons
- [ ] **API-05**: GET /api/dashboard-metrics returns summary counts (total scans, phishing, scam, safe)
- [ ] **API-06**: GET /api/health returns backend health status
- [ ] **API-07**: All API endpoints return consistent JSON error responses for invalid input

### Dashboard & UI

- [ ] **UI-01**: Dashboard page displays total scans, phishing detections, scam detections, safe detections as summary cards
- [ ] **UI-02**: URL Scanner page with URL input field, scan button, and result display area
- [ ] **UI-03**: Message Scanner page with textarea for SMS/email text, scan button, and result display area
- [ ] **UI-04**: Result display shows classification badge (color-coded: green/yellow/red), risk score, threat level, and explanation list
- [ ] **UI-05**: History page shows past scans in a table with scan type, content preview, prediction, risk score, timestamp
- [ ] **UI-06**: Navigation between Dashboard, URL Scanner, Message Scanner, and History sections
- [ ] **UI-07**: Responsive design that works in Chrome, Edge, and Firefox
- [ ] **UI-08**: Loading indicators during scan analysis

### Performance

- [ ] **PERF-01**: URL analysis completes in under 3 seconds
- [ ] **PERF-02**: Message analysis completes in under 5 seconds

## v2 Requirements (Deferred)

- [ ] Analytics charts and visual scan trend summaries
- [ ] Batch URL scanning (multiple URLs at once)
- [ ] Export scan history to CSV
- [ ] Detailed scan drill-down modal with full analysis breakdown

## Out of Scope

- Browser extension — requires separate codebase, exceeds MVP scope
- WhatsApp/inbox integration — OAuth complexity, scope creep
- Live threat intelligence feeds (VirusTotal, PhishTank API) — external dependency
- User authentication — not required per PRD, simplifies MVP
- Deep learning models (TensorFlow/PyTorch) — overkill for this dataset, requires GPU
- Multi-language detection — training data scarcity
- Real-time URL monitoring — requires browser extension
- Production deployment — local demo environment only
- Malware scanning — different domain entirely

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| DB-01, DB-02, DB-03 | Phase 1 | Pending |
| ML-01 through ML-05 | Phase 2 | Pending |
| URL-01 through URL-06 | Phase 3 | Pending |
| MSG-01 through MSG-06 | Phase 4 | Pending |
| API-01 through API-07 | Phase 3, 4 | Pending |
| UI-01 through UI-08 | Phase 5 | Pending |
| PERF-01, PERF-02 | Phase 3, 4 | Pending |

---
*Requirements defined: 2026-05-19*
*Total v1 requirements: 33*
