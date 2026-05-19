# Feature Research

**Domain:** Phishing URL & Scam Message Detection
**Researched:** 2026-05-19
**Confidence:** HIGH

## Feature Landscape

### Table Stakes (Users Expect These)

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| URL input & scan | Core purpose of the tool | MEDIUM | Need validation, parsing, feature extraction, scoring |
| Threat classification (Safe/Suspicious/Phishing) | Users need clear verdict | LOW | Map risk score to 3-tier classification |
| Risk score display | Users want confidence level | LOW | Numeric 0-100 score from heuristic weights |
| Explanation of detection | Core differentiator — users need to understand WHY | MEDIUM | Rule-based reason generation for each flagged feature |
| Message/SMS input & scan | Second core capability | HIGH | Full ML pipeline: preprocessing → TF-IDF → classification |
| Scan history | Users revisit past scans | MEDIUM | MySQL storage + retrieval API + UI display |
| Dashboard with metrics | Overview of activity | MEDIUM | Aggregate counts from scan_records table |
| Error handling for invalid input | Users will submit garbage | LOW | URL validation, empty input checks, meaningful error messages |

### Differentiators (Competitive Advantage)

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| Explainable threat reasons | Most tools give binary verdict; PhishGuard explains WHY | MEDIUM | Rule-based explanations mapped to detected indicators |
| Dual scanning (URL + Message) | Single tool for both attack vectors | HIGH | Two separate analysis engines in one dashboard |
| Visual threat indicators | Color-coded risk levels, progress bars | LOW | CSS/Bootstrap styling for threat visualization |
| Detailed scan view | Drill into any past scan for full analysis | LOW | History detail API + modal/page |
| Analytics charts | Visual summary of scan patterns | MEDIUM | Chart.js or similar for dashboard charts |

### Anti-Features (Commonly Requested, Often Problematic)

| Feature | Why Requested | Why Problematic | Alternative |
|---------|---------------|-----------------|-------------|
| Real-time URL monitoring | "Scan all my browsing" | Requires browser extension, privacy concerns, massive scope | On-demand URL scanning |
| Email inbox integration | "Scan my inbox automatically" | OAuth complexity, security liability, scope creep | Copy-paste message text |
| Live threat intelligence feeds | "Use VirusTotal/PhishTank API" | External dependency, API keys, rate limits, adds latency | Local heuristic + ML analysis |
| User accounts & auth | "Save my personal history" | Authentication complexity, password management, session security | Anonymous scan history (shared) |
| Multi-language detection | "Detect scams in Hindi/other languages" | Training data scarcity, tokenization complexity | English-only for MVP |

## Feature Dependencies

```
URL Scan Engine
    └──requires──> URL Feature Extraction
                       └──requires──> URL Validation

Message Scan Engine
    └──requires──> ML Model (trained + serialized)
                       └──requires──> Dataset + Training Pipeline

Scan History
    └──requires──> MySQL Database Schema
                       └──requires──> Database Connection

Dashboard Metrics
    └──requires──> Scan History (aggregation queries)

Explainability Engine
    └──enhances──> URL Scan Engine
    └──enhances──> Message Scan Engine
```

### Dependency Notes

- **Dashboard Metrics requires Scan History:** Can't aggregate what isn't stored
- **Message Scan requires trained ML model:** Model must be trained and serialized before the API can serve predictions
- **Explainability enhances both engines:** Can be built incrementally alongside each scanner

## MVP Definition

### Launch With (v1)

- [ ] URL scanning with heuristic analysis + classification + explanations
- [ ] Message scanning with ML classification + explanations
- [ ] Dashboard with scan metrics summary
- [ ] Scan history storage and retrieval
- [ ] RESTful API endpoints
- [ ] Error handling for invalid inputs
- [ ] MySQL persistence

### Add After Validation (v1.x)

- [ ] Analytics charts (visual scan trends) — after core scanning works
- [ ] Batch URL scanning — after single URL scanning is stable
- [ ] Export scan history to CSV — after history UI is polished

### Future Consideration (v2+)

- [ ] Browser extension — requires separate codebase
- [ ] Real-time threat feeds integration — external API dependency
- [ ] Multi-language support — dataset and tokenizer changes
- [ ] User authentication — full auth system

## Feature Prioritization Matrix

| Feature | User Value | Implementation Cost | Priority |
|---------|------------|---------------------|----------|
| URL scanning + classification | HIGH | MEDIUM | P1 |
| URL explainability | HIGH | MEDIUM | P1 |
| Message scanning + ML | HIGH | HIGH | P1 |
| Message explainability | HIGH | LOW | P1 |
| Dashboard metrics | MEDIUM | LOW | P1 |
| Scan history | MEDIUM | MEDIUM | P1 |
| Error handling | MEDIUM | LOW | P1 |
| Analytics charts | LOW | MEDIUM | P2 |
| Detailed scan drill-down | LOW | LOW | P2 |

## Competitor Feature Analysis

| Feature | VirusTotal | Google Safe Browsing | PhishTank | PhishGuard (Ours) |
|---------|-----------|---------------------|-----------|-------------------|
| URL scanning | Multi-engine (60+) | Binary safe/unsafe | Community-reported | Rule-based heuristics |
| Message scanning | No | No | No | TF-IDF + Logistic Regression |
| Explainability | Vendor scores only | No explanation | Community comments | Human-readable reasons |
| Scan history | Yes (with account) | No | No | Yes (MySQL-backed) |
| Cost | Free tier limited | Free API | Free | Free (self-hosted) |

## Sources

- Web research: phishing detection features and best practices
- VirusTotal, Google Safe Browsing, PhishTank — competitor analysis
- SMS Spam Collection Dataset documentation

---
*Feature research for: Phishing URL & Scam Message Detection*
*Researched: 2026-05-19*
