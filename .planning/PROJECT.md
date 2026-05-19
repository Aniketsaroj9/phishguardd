# PhishGuard

## What This Is

PhishGuard is a web-based cybersecurity application that detects phishing URLs and scam messages (SMS/email) using a hybrid approach combining rule-based threat analysis and machine learning classification. Users submit suspicious URLs or text content and receive a risk assessment, threat classification, and explainable human-readable reasoning. Built for both non-technical users who need fast threat checks and cybersecurity learners who want to understand detection logic.

## Core Value

Users can paste a suspicious URL or message and instantly get an understandable, explainable threat assessment — no cybersecurity expertise required.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] URL submission with validation and threat analysis using rule-based heuristics
- [ ] URL classification as Safe / Suspicious / Phishing with risk scoring
- [ ] Human-readable explanation generation for URL threat detections
- [ ] SMS/email message submission and ML-based scam analysis
- [ ] Message classification as Safe / Scam with confidence scoring
- [ ] Human-readable explanation generation for message detections
- [ ] Dashboard with summary metrics (total scans, phishing detections, scam detections, safe detections)
- [ ] Scan history storage in MySQL with retrieval
- [ ] RESTful API endpoints (analyze-url, analyze-message, history, dashboard-metrics, health)
- [ ] Error handling for invalid input with user-friendly messages
- [ ] Persistent MySQL storage with scan_records and threat_reasons tables

### Out of Scope

- Browser extension — MVP scope, not needed for demo
- WhatsApp integration — complexity exceeds timeline
- Live inbox scanning — requires auth integrations out of scope
- Malware scanning — different domain, out of scope
- Deep learning models — feasibility constraint, using traditional ML
- Real-time threat intelligence feeds — external dependency, not needed for MVP
- User authentication — not required per PRD
- Production deployment — local demo environment only
- Multi-language support — English only for MVP

## Context

- **Target users**: General internet users, students (fake scholarship/internship scams), non-technical users, cybersecurity learners
- **Key personas**: Rahul (student checking suspicious academic emails), Priya (banking user verifying scam SMS), Aman (learner studying phishing indicators)
- **Explainability is the core differentiator** — not just predictions, but human-readable reasons why something is flagged
- **URL detection**: Rule-based heuristic scoring (suspicious keywords, URL length, dots, hyphens, HTTP/HTTPS, IP-based URLs, suspicious TLDs, unusual domain structure)
- **Message detection**: TF-IDF + Logistic Regression pipeline (preprocessing → tokenization → stopword removal → TF-IDF → classification)
- **Dataset candidates**: SMS Spam Collection Dataset, phishing/scam datasets
- **Architecture**: Modular client-server — User → Dashboard → Flask Backend → Analyzers → MySQL → Response
- **Runs on XAMPP** environment (localhost)

## Constraints

- **Timeline**: 15-day development window — limits scope to MVP features only
- **Tech Stack**: HTML/CSS/Bootstrap + JavaScript frontend, Python/Flask backend, scikit-learn/pandas/NLTK for ML, MySQL database
- **Hardware**: Must run on standard student hardware — no GPU requirements, no heavy dependencies
- **Accuracy**: 80%+ target for ML classifier — achievable with Logistic Regression + TF-IDF
- **Performance**: URL analysis under 3 seconds, message analysis under 5 seconds
- **Compatibility**: Must work in Chrome, Edge, Firefox
- **Development Tools**: Antigravity IDE, MySQL Workbench, GitHub

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Hybrid detection (rule-based URLs + ML messages) | URLs have clear structural indicators suited for rules; messages need NLP/ML for semantic analysis | — Pending |
| Rule-based explainability over SHAP/LIME | MVP feasibility — SHAP/LIME adds complexity without proportional benefit for this use case | — Pending |
| TF-IDF + Logistic Regression over deep learning | Runs on student hardware, 80%+ accuracy achievable, interpretable model | — Pending |
| No user authentication | Simplifies MVP, demo-focused, not production | — Pending |
| MySQL over SQLite | PRD specifies MySQL, XAMPP environment available | — Pending |
| Flask over Django | Lightweight, sufficient for API-focused backend, faster development | — Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-05-19 after initialization*
