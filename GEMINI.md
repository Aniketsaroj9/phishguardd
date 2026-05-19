<!-- GSD:project-start source:PROJECT.md -->
## Project

**PhishGuard**

PhishGuard is a web-based cybersecurity application that detects phishing URLs and scam messages (SMS/email) using a hybrid approach combining rule-based threat analysis and machine learning classification. Users submit suspicious URLs or text content and receive a risk assessment, threat classification, and explainable human-readable reasoning. Built for both non-technical users who need fast threat checks and cybersecurity learners who want to understand detection logic.

**Core Value:** Users can paste a suspicious URL or message and instantly get an understandable, explainable threat assessment — no cybersecurity expertise required.

### Constraints

- **Timeline**: 15-day development window — limits scope to MVP features only
- **Tech Stack**: HTML/CSS/Bootstrap + JavaScript frontend, Python/Flask backend, scikit-learn/pandas/NLTK for ML, MySQL database
- **Hardware**: Must run on standard student hardware — no GPU requirements, no heavy dependencies
- **Accuracy**: 80%+ target for ML classifier — achievable with Logistic Regression + TF-IDF
- **Performance**: URL analysis under 3 seconds, message analysis under 5 seconds
- **Compatibility**: Must work in Chrome, Edge, Firefox
- **Development Tools**: Antigravity IDE, MySQL Workbench, GitHub
<!-- GSD:project-end -->

<!-- GSD:stack-start source:research/STACK.md -->
## Technology Stack

## Recommended Stack
### Core Technologies
| Technology | Version | Purpose | Why Recommended |
|------------|---------|---------|-----------------|
| Python | 3.10+ | Backend language | De facto standard for ML/NLP work; Flask ecosystem; scikit-learn compatibility |
| Flask | 3.x | Web framework / API server | Lightweight, perfect for REST APIs; low overhead; simple routing; ideal for ML model serving |
| scikit-learn | 1.4+ | ML pipeline (TF-IDF + Logistic Regression) | Industry standard for classical ML; built-in pipelines; excellent documentation; runs on CPU |
| MySQL | 8.0+ | Persistent storage | Relational DB for scan history; ACID compliance; XAMPP bundled; well-suited for structured scan records |
| Bootstrap | 5.3 | Frontend CSS framework | Responsive grid; pre-built components; beginner-friendly; fast UI development |
### Supporting Libraries
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| pandas | 2.x | Data loading & preprocessing | Loading SMS Spam Collection CSV; feature engineering; data cleaning |
| NLTK | 3.8+ | NLP preprocessing | Tokenization, stopword removal, stemming for message text preprocessing |
| joblib | 1.3+ | Model serialization | Saving/loading trained TF-IDF vectorizer + Logistic Regression model to disk |
| mysql-connector-python | 8.x | MySQL driver for Python | Connecting Flask backend to MySQL database |
| flask-cors | 4.x | CORS handling | Allowing frontend (served separately) to call Flask API endpoints |
| re (stdlib) | — | Regex for URL parsing | Extracting URL features (protocol, domain, path, TLD) for heuristic analysis |
| urllib.parse (stdlib) | — | URL decomposition | Parsing URL components for feature extraction |
### Development Tools
| Tool | Purpose | Notes |
|------|---------|-------|
| XAMPP | Local MySQL + Apache server | Provides MySQL out of the box; use phpMyAdmin for DB management |
| MySQL Workbench | Database design & queries | Visual schema design; query testing |
| pip / venv | Python dependency management | Always use virtual environment to isolate dependencies |
| Jupyter Notebook | Model training & experimentation | Train and evaluate ML model before exporting to production |
## Installation
# Create virtual environment
# Core
# ML/NLP
# Download NLTK data
## Alternatives Considered
| Recommended | Alternative | When to Use Alternative |
|-------------|-------------|-------------------------|
| Flask | Django | When you need admin panel, ORM, and full-featured framework (overkill for this MVP) |
| Flask | FastAPI | When you need async support and auto-generated OpenAPI docs (unnecessary complexity here) |
| Logistic Regression | Random Forest / XGBoost | When dataset is larger and non-linear patterns dominate (LR is sufficient for 80%+ on SMS spam) |
| MySQL | SQLite | When deploying as single-file app with no separate DB server (simpler but PRD specifies MySQL) |
| Bootstrap | Tailwind CSS | When you want utility-first CSS with more customization (Bootstrap is faster for prototyping) |
| NLTK | spaCy | When you need production-grade NLP with better performance (heavier dependency, overkill for tokenization + stopwords) |
## What NOT to Use
| Avoid | Why | Use Instead |
|-------|-----|-------------|
| Deep learning (TensorFlow/PyTorch) | Overkill for this dataset size; GPU required; slow training; hard to explain | scikit-learn Logistic Regression |
| SHAP/LIME for explainability | Adds complexity without proportional benefit for rule-based URL analysis | Custom rule-based explanation engine |
| MongoDB | Scan records have fixed schema; relational queries needed for history/metrics | MySQL with structured tables |
| Raw SQL strings | SQL injection vulnerability | Parameterized queries with mysql-connector |
## Version Compatibility
| Package A | Compatible With | Notes |
|-----------|-----------------|-------|
| scikit-learn 1.4+ | joblib 1.3+ | Use joblib for model persistence (pickle has security issues) |
| Flask 3.x | Python 3.10+ | Flask 3 dropped Python 3.7 support |
| mysql-connector-python 8.x | MySQL 8.0+ | Ensure MySQL server version matches connector |
| Bootstrap 5.3 | Modern browsers | No jQuery dependency (dropped in Bootstrap 5) |
## Sources
- Web research: phishing URL detection Python Flask best practices 2025
- Web research: SMS spam detection TF-IDF logistic regression scikit-learn
- SMS Spam Collection Dataset (UCI/Kaggle) — 5,574 messages, ham/spam labeled
- scikit-learn official documentation — pipeline, TfidfVectorizer, LogisticRegression
<!-- GSD:stack-end -->

<!-- GSD:conventions-start source:CONVENTIONS.md -->
## Conventions

Conventions not yet established. Will populate as patterns emerge during development.
<!-- GSD:conventions-end -->

<!-- GSD:architecture-start source:ARCHITECTURE.md -->
## Architecture

Architecture not yet mapped. Follow existing patterns found in the codebase.
<!-- GSD:architecture-end -->

<!-- GSD:skills-start source:skills/ -->
## Project Skills

No project skills found. Add skills to any of: `.agent/skills/`, `.agents/skills/`, `.cursor/skills/`, or `.github/skills/` with a `SKILL.md` index file.
<!-- GSD:skills-end -->

<!-- GSD:workflow-start source:GSD defaults -->
## GSD Workflow Enforcement

Before using Edit, Write, or other file-changing tools, start work through a GSD command so planning artifacts and execution context stay in sync.

Use these entry points:
- `/gsd-quick` for small fixes, doc updates, and ad-hoc tasks
- `/gsd-debug` for investigation and bug fixing
- `/gsd-execute-phase` for planned phase work

Do not make direct repo edits outside a GSD workflow unless the user explicitly asks to bypass it.
<!-- GSD:workflow-end -->



<!-- GSD:profile-start -->
## Developer Profile

> Profile not yet configured. Run `/gsd-profile-user` to generate your developer profile.
> This section is managed by `generate-claude-profile` -- do not edit manually.
<!-- GSD:profile-end -->
