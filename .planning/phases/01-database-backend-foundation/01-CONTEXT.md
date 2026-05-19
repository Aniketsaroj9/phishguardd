# Phase 1: Database & Backend Foundation - Context

**Gathered:** 2026-05-19
**Status:** Ready for planning

<domain>
## Phase Boundary

Set up MySQL database schema (`phishguard_db` with `scan_records` and `threat_reasons` tables), Flask application skeleton with modular structure, CORS configuration, health endpoint, and consistent error handling. This phase delivers the infrastructure that all subsequent phases depend on.

</domain>

<decisions>
## Implementation Decisions

### Database Configuration
- **D-01:** MySQL credentials stored in `config.py` with sensible defaults for XAMPP localhost (host=localhost, user=root, password='', database=phishguard_db)
- **D-02:** Database and tables auto-create on app startup — app checks if `phishguard_db` exists, creates it and all tables if missing. Zero manual setup required.
- **D-03:** All queries use parameterized statements via mysql-connector-python. No string concatenation in SQL.

### Backend Structure
- **D-04:** Modular file structure — `app.py` as Flask entry point, separate modules for analyzers (`url_analyzer.py`, `message_analyzer.py`), database layer (`database.py`), explainer (`explainer.py`), and config (`config.py`)
- **D-05:** ML model artifacts live in `backend/ml/` directory (model.pkl, vectorizer.pkl, training script, dataset)
- **D-06:** Project structure follows architecture research: `backend/` for Python/Flask, `frontend/` for HTML/CSS/JS, `database/` for SQL scripts

### API Response Format
- **D-07:** (Agent's Discretion) Wrapped response format with `success`, `data`, and optional `error` fields. Every endpoint returns consistent JSON shape:
  - Success: `{"success": true, "data": {...}}`
  - Error: `{"success": false, "error": "message"}`
  - HTTP status codes used alongside (200 for success, 400 for bad input, 500 for server errors)

### Development Workflow
- **D-08:** Start with `python app.py` — Flask debug mode enabled (`debug=True`) for hot-reload during development
- **D-09:** CORS restricted to localhost only — `CORS(app, origins=["http://localhost"])` for security. Will include common XAMPP ports if needed.

### Agent's Discretion
- API response format (D-07): Agent chose wrapped format for consistency and frontend developer experience

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project Context
- `.planning/PROJECT.md` — Core value, constraints, key decisions
- `.planning/REQUIREMENTS.md` — DB-01, DB-02, DB-03, API-06, API-07 requirement details
- `.planning/ROADMAP.md` — Phase 1 success criteria and requirement mappings

### Research
- `.planning/research/ARCHITECTURE.md` — Project structure, component responsibilities, anti-patterns
- `.planning/research/STACK.md` — Technology versions, installation commands, compatibility
- `.planning/research/PITFALLS.md` — SQL injection prevention, CORS blocking, model file paths

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- None — greenfield project, no existing code

### Established Patterns
- None yet — this phase establishes the patterns all subsequent phases follow

### Integration Points
- Database layer will be imported by all analyzer modules in Phases 3-4
- Flask app skeleton will have routes added in Phases 3-4
- Config module will be imported across all backend modules

</code_context>

<specifics>
## Specific Ideas

- XAMPP provides MySQL on localhost with default root/no-password — config defaults should match this
- Database schema matches PRD exactly: `scan_records` (scan_id, scan_type, submitted_content, prediction, risk_score, threat_level, created_at) and `threat_reasons` (reason_id, scan_id, reason_text)
- Auto-create on startup is critical for demo — evaluator should be able to start the app and have everything work

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 01-database-backend-foundation*
*Context gathered: 2026-05-19*
