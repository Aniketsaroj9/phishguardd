---
phase: 5
plan: 01
title: "Frontend UI and API Integration"
wave: 1
depends_on: []
files_modified:
  - frontend/index.html
  - frontend/css/style.css
  - frontend/js/app.js
requirements:
  - UI-01
  - UI-02
  - UI-03
  - UI-04
  - UI-05
  - UI-06
  - UI-07
  - UI-08
autonomous: true
---

# Plan 01: Frontend UI and API Integration

<objective>
Build the responsive Single Page Application (SPA) frontend for PhishGuard. This includes the HTML layout, premium CSS styling, and JavaScript logic to interact with the backend API and manage view navigation.
</objective>

<must_haves>
- Navigation between Dashboard, URL Scanner, Message Scanner, and History.
- Dashboard fetches and displays summary metrics.
- URL Scanner and Message Scanner allow input, trigger API requests, and show loading states.
- Scan results display Threat Level, Risk Score, and Explanations.
- History fetches and displays a table of past scans.
- Premium, modern design using Bootstrap 5 and custom CSS.
</must_haves>

## Tasks

<task id="01.1" title="Build HTML Layout and Structure">
<read_first>
- .planning/phases/05-frontend-dashboard-ui/05-CONTEXT.md
</read_first>

<action>
Overwrite `frontend/index.html` with a complete SPA structure:
1. Include Bootstrap 5 CSS/JS, FontAwesome, and Google Fonts (Inter).
2. Add a top Navigation Bar with brand and links (Dashboard, URL Scan, Message Scan, History).
3. Create a main container with distinct `<section>` elements (all hidden by default except Dashboard):
   - `#dashboard-section`: 4 summary cards (Total, Phishing, Scam, Safe).
   - `#url-scan-section`: Input field, Scan button, and an empty `#url-result` container.
   - `#message-scan-section`: Textarea, SMS/Email radio buttons, Scan button, and an empty `#message-result` container.
   - `#history-section`: A table skeleton for `#history-table-body`.
4. Add loading spinner templates where necessary.
5. Link `css/style.css` and `js/app.js`.
</action>

<acceptance_criteria>
- `frontend/index.html` contains `<nav>` with navigation links.
- `frontend/index.html` contains `<section id="dashboard-section">`.
- `frontend/index.html` contains `<section id="url-scan-section">`.
- `frontend/index.html` contains `<section id="message-scan-section">`.
- `frontend/index.html` contains `<section id="history-section">`.
- `frontend/index.html` contains Bootstrap CDN links.
</acceptance_criteria>
</task>

<task id="01.2" title="Implement Premium CSS Styling">
<read_first>
- frontend/index.html
</read_first>

<action>
Overwrite `frontend/css/style.css` to add modern, premium styling:
1. Define CSS variables for colors: Primary blue, Safe (green), Suspicious (warning/orange), Phishing/Scam (danger/red), and background/text colors.
2. Apply `Inter` font to the body.
3. Style the Navigation bar to look modern and clean.
4. Style the Metric Cards (Dashboard) with hover effects, subtle shadows, and large numbers.
5. Style the Scan Results area: Create distinct classes for `.threat-safe`, `.threat-suspicious`, and `.threat-scam` that change borders/backgrounds accordingly. Include a risk score progress bar or visual indicator.
6. Hide sections that have the `.d-none` class.
7. Ensure responsive design (adjust padding/margins for mobile).
</action>

<acceptance_criteria>
- `frontend/css/style.css` contains `:root` variables for colors.
- `frontend/css/style.css` contains styles for `.threat-safe`, `.threat-suspicious`, and `.threat-scam`.
- `frontend/css/style.css` contains hover effects for cards.
</acceptance_criteria>
</task>

<task id="01.3" title="Implement JavaScript Logic and API Integration">
<read_first>
- frontend/index.html
- backend/app.py (for API endpoints)
</read_first>

<action>
Overwrite `frontend/js/app.js` with the frontend logic:
1. **Routing:** Add event listeners to nav links to show the target section and hide others. Add `.active` class to current nav item. Default to showing Dashboard.
2. **Dashboard:** On load (and on navigating to Dashboard), fetch `/api/dashboard-metrics` and update the 4 cards.
3. **URL Scanner:** On form submit, show loading spinner, fetch `/api/analyze-url` (POST `{"url": ...}`), hide spinner, and render the result (Threat badge, Risk Score, List of Reasons). Handle errors gracefully.
4. **Message Scanner:** On form submit, show loading spinner, fetch `/api/analyze-message` (POST `{"content": ..., "message_type": ...}`), hide spinner, and render the result.
5. **History:** On navigating to History, fetch `/api/history` and populate the table. Format dates nicely. Color code the Prediction column based on Threat Level.
6. Set base API URL to `http://localhost:5000`.
</action>

<acceptance_criteria>
- `frontend/js/app.js` contains a function to handle navigation/section switching.
- `frontend/js/app.js` contains `fetch('http://localhost:5000/api/analyze-url'` (or uses a base URL variable).
- `frontend/js/app.js` contains `fetch('http://localhost:5000/api/analyze-message'`.
- `frontend/js/app.js` contains DOM manipulation to render results (e.g., dynamically creating lists of reasons).
- `frontend/js/app.js` handles loading states during fetches.
</acceptance_criteria>
</task>

<verification>
1. Opening `frontend/index.html` in a browser displays the Dashboard.
2. Clicking navigation links switches views correctly.
3. The UI looks modern and polished.
4. Javascript functions for interacting with all 4 backend endpoints are present.
</verification>
