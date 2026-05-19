# Pitfalls Research

**Domain:** Phishing URL & Scam Message Detection
**Researched:** 2026-05-19
**Confidence:** HIGH

## Critical Pitfalls

### Pitfall 1: Overfitting ML Model to Training Data

**What goes wrong:**
Model achieves 95%+ accuracy on test split but fails on real-world SMS/email messages that differ from training distribution.

**Why it happens:**
SMS Spam Collection Dataset is small (5,574 messages) and biased toward specific spam patterns from 2012. Modern scams use different language.

**How to avoid:**
- Use stratified train/test split (80/20)
- Evaluate with Precision, Recall, F1 — not just accuracy
- Test with manually crafted modern scam messages (OTP fraud, KYC alerts, parcel scams)
- Use `ngram_range=(1, 2)` to capture multi-word patterns
- Set realistic accuracy target (80%+ not 99%)

**Warning signs:**
Training accuracy >> test accuracy by more than 5 percentage points

**Phase to address:**
ML model training phase — include diverse test cases in evaluation

---

### Pitfall 2: URL Heuristic False Positives on Legitimate Sites

**What goes wrong:**
Legitimate URLs with long paths, multiple subdomains, or keywords like "login" get flagged as phishing.

**Why it happens:**
Overly aggressive heuristic rules that trigger on common URL patterns (e.g., `accounts.google.com/login` flagged for "login" keyword + multiple dots).

**How to avoid:**
- Weight features carefully — no single feature should cause "Phishing" classification alone
- Use composite scoring with threshold tiers (Safe < 30, Suspicious 30-70, Phishing > 70)
- Test against known-good URLs (google.com, github.com, amazon.com)
- Include positive controls in testing

**Warning signs:**
Common legitimate websites scoring above "Safe" threshold

**Phase to address:**
URL analyzer phase — include false positive testing

---

### Pitfall 3: SQL Injection via Unsanitized Input

**What goes wrong:**
User submits a URL or message containing SQL injection payload, corrupting or exposing database.

**Why it happens:**
Using string concatenation for SQL queries instead of parameterized queries.

**How to avoid:**
- ALWAYS use parameterized queries with mysql-connector
- Never concatenate user input into SQL strings
- Validate and sanitize all inputs before database operations

**Warning signs:**
Any SQL query containing `f"..."` or `"..." + variable`

**Phase to address:**
Database setup phase — establish parameterized query pattern from the start

---

### Pitfall 4: Model File Not Found on App Startup

**What goes wrong:**
Flask app crashes on startup because `model.pkl` or `vectorizer.pkl` doesn't exist (not trained yet, wrong path, or not included in deployment).

**Why it happens:**
ML training is a separate step from app development. Developers forget to run training script, or use relative paths that break.

**How to avoid:**
- Include pre-trained model files in the repository
- Use absolute/configurable paths for model files
- Add startup check: if model files missing, log clear error message
- Document the training step in README

**Warning signs:**
`FileNotFoundError` or `ModuleNotFoundError` at app startup

**Phase to address:**
ML training phase — commit trained model files; app setup phase — add model existence check

---

### Pitfall 5: CORS Blocking Frontend-Backend Communication

**What goes wrong:**
Frontend JavaScript fetch() calls to Flask API fail with CORS error. Dashboard appears broken but backend is actually working fine.

**Why it happens:**
Flask doesn't include CORS headers by default. Frontend served from different origin (e.g., file:// or different port) than Flask API.

**How to avoid:**
- Install and configure flask-cors from day one
- Test API endpoints independently (Postman/curl) before building frontend
- Use consistent origin configuration

**Warning signs:**
"Access-Control-Allow-Origin" errors in browser console

**Phase to address:**
Backend setup phase — configure CORS immediately

---

### Pitfall 6: Explanation-Prediction Mismatch

**What goes wrong:**
Explanations say "URL flagged for suspicious TLD" but the classification says "Safe", confusing users.

**Why it happens:**
Explanation engine and scoring engine are not synchronized — different thresholds or logic paths.

**How to avoid:**
- Generate explanations FROM the same analysis that produces the score
- Pass reasons through the same function that calculates the score
- Never generate explanations separately from classification

**Warning signs:**
Any code path where score calculation and reason generation are in different functions without shared state

**Phase to address:**
URL analyzer and explainability engine — tight coupling between scoring and explanation

## Technical Debt Patterns

| Shortcut | Immediate Benefit | Long-term Cost | When Acceptable |
|----------|-------------------|----------------|-----------------|
| Global MySQL connection | Simple setup | Connection leaks under concurrency | MVP with single user |
| Hardcoded heuristic weights | Fast implementation | Can't tune without code changes | Always for this project scope |
| Single model file (no versioning) | Simple deployment | Can't A/B test or rollback models | MVP scope |
| No input length limits | Simpler validation | Potential DoS via huge payloads | MVP (add limits before any deployment) |

## Security Mistakes

| Mistake | Risk | Prevention |
|---------|------|------------|
| Raw SQL queries | SQL injection, data breach | Parameterized queries everywhere |
| Storing submitted URLs without sanitization | XSS when displaying in history | HTML-escape all user content in frontend |
| No input validation on API endpoints | Server crashes, unexpected behavior | Validate type, length, format before processing |
| Exposing MySQL credentials in frontend code | Database compromise | Keep all DB access server-side only |

## UX Pitfalls

| Pitfall | User Impact | Better Approach |
|---------|-------------|-----------------|
| Binary Safe/Phishing only | Users don't know what to do with borderline cases | 3-tier classification with color coding (green/yellow/red) |
| Technical jargon in explanations | Non-technical users don't understand "TLD" or "heuristic" | Plain language: "This website uses an uncommon domain ending (.xyz)" |
| No visual threat indicators | Users miss the classification result | Color-coded badges, progress bars, icons for threat level |
| Slow response with no feedback | Users think the app is broken | Loading spinner during analysis |

## "Looks Done But Isn't" Checklist

- [ ] **URL Scanner:** Test with URLs containing special characters (&, #, ?, =)
- [ ] **URL Scanner:** Test with very long URLs (200+ characters)
- [ ] **URL Scanner:** Test with IP-based URLs (http://192.168.1.1/login)
- [ ] **Message Scanner:** Test with empty/very short messages
- [ ] **Message Scanner:** Test with very long messages (1000+ characters)
- [ ] **History:** Verify timestamps display in user-friendly format
- [ ] **Dashboard:** Verify metrics update after new scans
- [ ] **API:** Verify JSON error responses for all error cases (not HTML error pages)
- [ ] **Database:** Verify threat_reasons are linked correctly to scan_records

## Pitfall-to-Phase Mapping

| Pitfall | Prevention Phase | Verification |
|---------|------------------|--------------|
| ML overfitting | ML Training | F1 score > 0.80 on test set + manual test with modern scams |
| URL false positives | URL Analyzer | Test against 10+ known legitimate URLs |
| SQL injection | Database Setup | Code review: zero string concatenation in SQL |
| Missing model files | ML Training + Backend Setup | App startup succeeds without manual intervention |
| CORS blocking | Backend Setup | Frontend can call all API endpoints without errors |
| Explanation mismatch | Explainability Engine | Score and reasons generated from same analysis pass |

## Sources

- Web research: phishing URL detection common mistakes pitfalls
- Web research: ML classification false positives rule-based
- OWASP SQL Injection Prevention Cheat Sheet
- scikit-learn model persistence documentation

---
*Pitfalls research for: Phishing URL & Scam Message Detection*
*Researched: 2026-05-19*
