# Phase 5: Frontend Dashboard & UI - Context

**Gathered:** 2026-05-19
**Status:** Ready for planning

<domain>
## Phase Boundary

Build the visual interface for PhishGuard. This includes a Dashboard for metrics, a URL Scanner view, a Message Scanner view, and a History view. The frontend will communicate with the Flask API built in Phases 1-4.

</domain>

<decisions>
## Implementation Decisions

### Architecture & Stack
- **D-01:** (Agent's Discretion) Use a Single Page Application (SPA) architecture using vanilla HTML/CSS/JS. No build step (React/Vue/Webpack) is required for this MVP, keeping it aligned with the "student hardware / simple" constraint.
- **D-02:** (Agent's Discretion) Use Bootstrap 5 via CDN for rapid, responsive layout.
- **D-03:** (Agent's Discretion) Use FontAwesome via CDN for iconography.

### UI Structure & Navigation
- **D-04:** (Agent's Discretion) A fixed sidebar or top navbar containing links: Dashboard, URL Scanner, Message Scanner, Scan History.
- **D-05:** (Agent's Discretion) Navigating between sections simply hides/shows standard `<section>` elements in `index.html`.

### Aesthetics & Design
- **D-06:** (Agent's Discretion) Follow the "Premium Design" guidelines: use modern typography (e.g., Inter via Google Fonts), subtle shadows, rounded corners, and a clean color palette (e.g., deep blue primary, red/yellow/green for threat levels).
- **D-07:** (Agent's Discretion) Color-coding: Safe = Green, Suspicious = Yellow/Orange, Phishing/Scam = Red.

### Component Behaviors
- **D-08:** (Agent's Discretion) Scan Results should clearly display the Threat Level badge, Risk Score progress bar/dial, and a list of Reasons (explanations).
- **D-09:** (Agent's Discretion) Show loading spinners while awaiting API responses.
- **D-10:** (Agent's Discretion) On page load, fetch Dashboard Metrics and populate the summary cards.

### Agent's Discretion
User stated "lets build" and "continue", deferring all specific UI design choices to the agent.

</decisions>

<canonical_refs>
## Canonical References

### Project Context
- `.planning/REQUIREMENTS.md` — UI-01 through UI-08
- `.planning/ROADMAP.md` — Phase 5 success criteria

</canonical_refs>

---

*Phase: 05-frontend-dashboard-ui*
*Context gathered: 2026-05-19*
