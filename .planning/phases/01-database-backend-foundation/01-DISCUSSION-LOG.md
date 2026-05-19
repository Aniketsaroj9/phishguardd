# Phase 1: Database & Backend Foundation - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-05-19
**Phase:** 01-database-backend-foundation
**Areas discussed:** Database Configuration, Backend Structure, API Response Format, Development Workflow

---

## Database Configuration

| Option | Description | Selected |
|--------|-------------|----------|
| Simple config.py | Credentials in config.py with XAMPP defaults | ✓ |
| Environment variables | .env file with python-dotenv | |
| Hardcoded in app.py | Direct credentials in main file | |

**User's choice:** Simple config.py (Recommended)

| Option | Description | Selected |
|--------|-------------|----------|
| Auto-create on startup | App checks/creates DB and tables automatically | ✓ |
| Manual SQL script | User runs schema.sql via phpMyAdmin | |

**User's choice:** Auto-create on startup (Recommended)

---

## Backend Structure

| Option | Description | Selected |
|--------|-------------|----------|
| Modular with separate files | app.py entry, separate analyzer/db/config modules | ✓ |
| Single app.py | Everything in one file | |
| Flask Blueprints | Full blueprint-based modular app | |

**User's choice:** Modular with separate files (Recommended)

| Option | Description | Selected |
|--------|-------------|----------|
| backend/ml/ directory | Separate folder for model artifacts | ✓ |
| backend/models/ | Alongside database models | |

**User's choice:** backend/ml/ directory (Recommended)

---

## API Response Format

| Option | Description | Selected |
|--------|-------------|----------|
| Wrapped with status | {success, data, error} envelope | ✓ |
| Flat/direct | Data directly, HTTP status for errors | |
| Envelope with metadata | Include timestamp, request_id | |

**User's choice:** "Do what you like" — Agent selected wrapped with status

---

## Development Workflow

| Option | Description | Selected |
|--------|-------------|----------|
| python app.py with debug mode | Simple, hot-reload built in | ✓ |
| Run script (run.bat) | Batch file for venv + Flask | |
| flask run with .flaskenv | Standard but more config | |

**User's choice:** python app.py with debug mode (Recommended)

| Option | Description | Selected |
|--------|-------------|----------|
| Allow all origins | CORS(app) allows everything | |
| Restrict to localhost only | CORS(app, origins=["http://localhost"]) | ✓ |

**User's choice:** Restrict to localhost only

---

## Agent's Discretion

- API response format — user deferred to agent, agent chose wrapped format

## Deferred Ideas

None
