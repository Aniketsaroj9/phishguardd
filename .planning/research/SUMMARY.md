# Project Research Summary

**Project:** PhishGuard
**Domain:** Phishing URL & Scam Message Detection (Cybersecurity Web App)
**Researched:** 2026-05-19
**Confidence:** HIGH

## Executive Summary

PhishGuard is a hybrid cybersecurity detection system combining rule-based URL heuristics with machine learning text classification. Research confirms this is a well-understood domain with established patterns: URL feature extraction + weighted scoring for phishing detection, and TF-IDF + Logistic Regression for SMS/email scam classification. The key differentiator — human-readable explainability — is best implemented via rule-based reason mapping rather than complex XAI frameworks.

The recommended approach builds the system bottom-up: database schema → ML model training → backend API → URL analyzer → message classifier → explainability → frontend dashboard. This ordering respects dependencies (ML model must exist before the API can serve predictions) and allows early validation of core detection logic before building the UI.

Key risks center on ML model overfitting to the small training dataset (5,574 messages), URL heuristic false positives on legitimate sites, and explanation-prediction mismatches. All are mitigable with proper evaluation, testing, and tight coupling between scoring and explanation engines.

## Key Findings

### Recommended Stack

Python/Flask backend with scikit-learn for ML, MySQL for persistence, and Bootstrap frontend. This stack is ideal because it's lightweight, runs on student hardware, and all components are well-documented with large communities.

**Core technologies:**
- Python 3.10+ / Flask 3.x: Backend + API — lightweight, perfect for ML model serving
- scikit-learn 1.4+: TF-IDF + Logistic Regression pipeline — achieves 80%+ on SMS spam
- MySQL 8.0+: Persistent storage — XAMPP-bundled, relational queries for history/metrics
- Bootstrap 5.3: Frontend — responsive, fast prototyping, no jQuery dependency

### Expected Features

**Must have (table stakes):**
- URL scanning with heuristic analysis + 3-tier classification
- Message scanning with ML classification
- Explainable threat reasons (human-readable)
- Dashboard with scan metrics
- Scan history with retrieval

**Should have (competitive):**
- Visual threat indicators (color-coded risk levels)
- Detailed scan drill-down view
- Analytics charts

**Defer (v2+):**
- Browser extension, live threat feeds, user authentication, multi-language

### Architecture Approach

Modular 3-layer architecture: presentation (HTML/Bootstrap/JS), application (Flask API + analyzers), data (MySQL). Each analysis type (URL, message) has its own analyzer module, with a shared explainability engine. ML model is trained once, serialized, and loaded at Flask startup.

**Major components:**
1. URL Analyzer — heuristic feature extraction + weighted scoring
2. Message Classifier — serialized TF-IDF + Logistic Regression pipeline
3. Explainability Engine — rule-based reason generation from detected indicators
4. Flask API — REST endpoints routing to analyzers
5. MySQL Database — scan_records + threat_reasons tables

### Critical Pitfalls

1. **ML overfitting** — Small dataset, old spam patterns. Mitigate with stratified splits, F1 evaluation, modern test cases
2. **URL false positives** — Legitimate sites flagged by aggressive rules. Mitigate with composite scoring, threshold tiers
3. **SQL injection** — User input in queries. Mitigate with parameterized queries everywhere
4. **CORS blocking** — Frontend can't reach API. Mitigate with flask-cors from day one
5. **Explanation mismatch** — Reasons don't match classification. Mitigate with tight coupling

## Implications for Roadmap

Based on research, suggested phase structure:

### Phase 1: Foundation (Database + Backend Setup)
**Rationale:** Everything depends on the database schema and Flask API server
**Delivers:** MySQL schema, Flask app skeleton, CORS config, health endpoint
**Addresses:** Database persistence, API infrastructure
**Avoids:** SQL injection (parameterized queries from start), CORS blocking

### Phase 2: ML Model Training
**Rationale:** Message analyzer depends on trained model; must exist before API integration
**Delivers:** Trained TF-IDF + Logistic Regression model, evaluation metrics, serialized artifacts
**Addresses:** Message classification capability
**Avoids:** ML overfitting (proper evaluation), missing model files (committed artifacts)

### Phase 3: URL Analysis Engine
**Rationale:** Core detection capability #1; independent of ML model
**Delivers:** URL feature extraction, heuristic scoring, classification, explanation generation
**Addresses:** URL scanning + explainability
**Avoids:** False positives (composite scoring), explanation mismatch (tight coupling)

### Phase 4: Message Analysis Engine
**Rationale:** Core detection capability #2; depends on Phase 2 model
**Delivers:** Message preprocessing, ML prediction, explanation generation, API endpoint
**Addresses:** Message scanning + explainability
**Avoids:** Overfitting (diverse test cases in verification)

### Phase 5: Frontend Dashboard
**Rationale:** UI depends on all API endpoints being functional
**Delivers:** Dashboard, URL scanner UI, message scanner UI, history view, analytics
**Addresses:** All UI requirements
**Avoids:** UX pitfalls (clear visual indicators, plain language)

### Phase Ordering Rationale

- Database first because all data storage depends on schema
- ML training before message analysis because the API needs serialized model files
- URL analysis independent of ML — can be built in parallel with ML training if desired
- Frontend last because it consumes all API endpoints

### Research Flags

Phases likely needing deeper research during planning:
- **Phase 2:** ML training — need to verify dataset format, preprocessing pipeline specifics
- **Phase 5:** Frontend — design decisions for dashboard layout, chart library selection

Phases with standard patterns (skip research-phase):
- **Phase 1:** Database + Flask setup — well-documented, established patterns
- **Phase 3:** URL heuristics — straightforward feature extraction

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | PRD specifies stack; all technologies well-documented |
| Features | HIGH | Clear PRD requirements; competitor analysis validates approach |
| Architecture | HIGH | Standard Flask + ML serving pattern; well-established |
| Pitfalls | HIGH | Common issues well-documented in cybersecurity ML literature |

**Overall confidence:** HIGH

### Gaps to Address

- Dataset quality: SMS Spam Collection is from 2012 — may need supplementation with modern scam patterns for evaluation
- Heuristic weight tuning: No established standard weights — will need iterative testing
- MySQL connection management: Need to decide on connection pooling strategy during implementation

## Sources

### Primary (HIGH confidence)
- scikit-learn documentation — TfidfVectorizer, LogisticRegression, Pipeline
- Flask documentation — routing, JSON responses, CORS
- MySQL Connector/Python documentation — parameterized queries

### Secondary (MEDIUM confidence)
- Web research: phishing URL detection Python Flask best practices 2025
- Web research: SMS spam detection TF-IDF logistic regression
- SMS Spam Collection Dataset (UCI/Kaggle) — 5,574 labeled messages

### Tertiary (LOW confidence)
- Heuristic weight values — will need empirical tuning during implementation

---
*Research completed: 2026-05-19*
*Ready for roadmap: yes*
