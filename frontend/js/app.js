/**
 * PhishGuard - Frontend Logic
 */

// API base URL: set window.PHISHGUARD_API_BASE in config.js (see config.example.js)
// for production deploys. Falls back to localhost for local development.
const API_BASE = window.PHISHGUARD_API_BASE || 'http://localhost:5000/api';

// DOM Elements
const sections = {
    dashboard: document.getElementById('dashboard-section'),
    urlScan: document.getElementById('url-scan-section'),
    messageScan: document.getElementById('message-scan-section'),
    history: document.getElementById('history-section')
};

const navLinks = document.querySelectorAll('.nav-link, .navbar-brand');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setupNavigation();
    setupForms();
    loadDashboardMetrics();
    
    // Refresh buttons
    document.getElementById('refresh-dashboard').addEventListener('click', loadDashboardMetrics);
    document.getElementById('refresh-history').addEventListener('click', loadHistory);
});

// ==========================================
// Navigation & Routing
// ==========================================

function setupNavigation() {
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('data-target');
            if(!targetId) return;
            
            // Update active link
            navLinks.forEach(l => l.classList.remove('active'));
            if(link.classList.contains('nav-link')) {
                link.classList.add('active');
            } else {
                // If brand clicked, set dashboard as active
                document.querySelector('.nav-link[data-target="dashboard-section"]').classList.add('active');
            }

            // Hide all sections
            Object.values(sections).forEach(sec => sec.classList.add('d-none'));
            
            // Show target section
            document.getElementById(targetId).classList.remove('d-none');

            // Trigger specific section loads
            if(targetId === 'dashboard-section') loadDashboardMetrics();
            if(targetId === 'history-section') loadHistory();
            
            // Close mobile menu if open
            const navbarCollapse = document.getElementById('navbarNav');
            if (navbarCollapse.classList.contains('show')) {
                const bsCollapse = new bootstrap.Collapse(navbarCollapse, {toggle: false});
                bsCollapse.hide();
            }
        });
    });
}

// ==========================================
// API Calls
// ==========================================

async function fetchAPI(endpoint, method = 'GET', body = null) {
    try {
        const options = {
            method,
            headers: { 'Content-Type': 'application/json' }
        };
        if (body) options.body = JSON.stringify(body);

        const response = await fetch(`${API_BASE}${endpoint}`, options);
        const data = await response.json();
        
        if (!response.ok || !data.success) {
            throw new Error(data.error || 'API Request Failed');
        }
        return data.data;
    } catch (error) {
        console.error(`API Error (${endpoint}):`, error);
        throw error;
    }
}

// ==========================================
// Dashboard
// ==========================================

async function loadDashboardMetrics() {
    try {
        const btn = document.getElementById('refresh-dashboard');
        btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Refreshing...';
        btn.disabled = true;

        const metrics = await fetchAPI('/dashboard-metrics');
        
        document.getElementById('metric-total').textContent = metrics.total;
        document.getElementById('metric-safe').textContent = metrics.safe;
        document.getElementById('metric-suspicious').textContent = metrics.scam; // Map scam to suspicious internally if needed, but let's use the explicit names
        
        // Combine phishing and scam for the red card
        const dangerousCount = (metrics.phishing || 0) + (metrics.scam || 0);
        document.getElementById('metric-phishing-scam').textContent = dangerousCount;

    } catch (error) {
        showErrorToast('Failed to load dashboard metrics');
    } finally {
        const btn = document.getElementById('refresh-dashboard');
        btn.innerHTML = '<i class="fa-solid fa-rotate-right"></i> Refresh';
        btn.disabled = false;
    }
}

// ==========================================
// Scanners
// ==========================================

function setupForms() {
    // URL Scan Form
    document.getElementById('url-scan-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const url = document.getElementById('url-input').value;
        const resultContainer = document.getElementById('url-result-container');
        const loadingDiv = document.getElementById('url-loading');
        
        resultContainer.innerHTML = '';
        resultContainer.classList.add('d-none');
        loadingDiv.classList.remove('d-none');

        try {
            const result = await fetchAPI('/analyze-url', 'POST', { url });
            renderResult(result, resultContainer);
        } catch (error) {
            resultContainer.innerHTML = `<div class="alert alert-danger"><i class="fa-solid fa-circle-exclamation me-2"></i>${error.message}</div>`;
            resultContainer.classList.remove('d-none');
        } finally {
            loadingDiv.classList.add('d-none');
        }
    });

    // Message Scan Form
    document.getElementById('message-scan-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const content = document.getElementById('message-input').value;
        const messageType = document.querySelector('input[name="messageType"]:checked').value;
        const resultContainer = document.getElementById('message-result-container');
        const loadingDiv = document.getElementById('message-loading');
        
        resultContainer.innerHTML = '';
        resultContainer.classList.add('d-none');
        loadingDiv.classList.remove('d-none');

        try {
            const result = await fetchAPI('/analyze-message', 'POST', { content, message_type: messageType });
            renderResult(result, resultContainer);
        } catch (error) {
            resultContainer.innerHTML = `<div class="alert alert-danger"><i class="fa-solid fa-circle-exclamation me-2"></i>${error.message}</div>`;
            resultContainer.classList.remove('d-none');
        } finally {
            loadingDiv.classList.add('d-none');
        }
    });
}

function renderResult(result, container) {
    const template = document.getElementById('result-card-template').content.cloneNode(true);
    const card = template.querySelector('.result-card');
    
    // Set Threat Class
    const threatClass = `threat-${result.threat_level.toLowerCase()}`;
    card.classList.add(threatClass);

    // Set Badge
    const badge = template.querySelector('.threat-badge');
    badge.textContent = result.threat_level.toUpperCase();
    
    let icon = 'fa-check-circle';
    if(result.threat_level === 'Suspicious') icon = 'fa-triangle-exclamation';
    if(['Phishing', 'Scam'].includes(result.threat_level)) icon = 'fa-radiation';
    badge.innerHTML = `<i class="fa-solid ${icon} me-1"></i> ${result.threat_level.toUpperCase()}`;

    // Set Content Preview
    const preview = template.querySelector('.content-preview');
    preview.textContent = result.url || result.content;

    // Set Risk Score
    const scoreText = template.querySelector('.risk-score-text');
    scoreText.textContent = Math.round(result.risk_score);

    // Populate Reasons
    const reasonsList = template.querySelector('.reasons-list');
    result.reasons.forEach(reason => {
        const li = document.createElement('li');
        li.className = 'list-group-item bg-transparent';
        li.innerHTML = `<i class="fa-solid fa-angle-right me-2 text-primary"></i> ${reason}`;
        reasonsList.appendChild(li);
    });

    container.appendChild(template);
    container.classList.remove('d-none');
}

// ==========================================
// History
// ==========================================

async function loadHistory() {
    const tbody = document.getElementById('history-table-body');
    
    try {
        const btn = document.getElementById('refresh-history');
        btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Refreshing...';
        btn.disabled = true;

        const data = await fetchAPI('/history?limit=50');
        
        tbody.innerHTML = '';
        
        if (!data.records || data.records.length === 0) {
            tbody.innerHTML = `<tr><td colspan="5" class="text-center py-4 text-muted">No scan history found.</td></tr>`;
            return;
        }

        data.records.forEach(record => {
            const tr = document.createElement('tr');
            
            // Format Date
            const date = new Date(record.created_at);
            const dateStr = date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
            
            // Threat Badge Style
            const threatLower = record.threat_level.toLowerCase();
            let badgeClass = 'badge-soft-safe';
            if (threatLower === 'suspicious') badgeClass = 'badge-soft-suspicious';
            if (['phishing', 'scam'].includes(threatLower)) badgeClass = 'badge-soft-danger';

            // Content preview (truncate)
            let preview = record.submitted_content;
            if(preview.length > 50) preview = preview.substring(0, 47) + '...';

            tr.innerHTML = `
                <td class="ps-4 fw-bold text-muted">${record.scan_type}</td>
                <td class="font-monospace small text-truncate" style="max-width: 300px;">${preview}</td>
                <td><span class="badge rounded-pill ${badgeClass} px-3">${record.threat_level}</span></td>
                <td><span class="fw-bold">${record.risk_score}</span><span class="text-muted small">/100</span></td>
                <td class="text-muted small">${dateStr}</td>
            `;
            tbody.appendChild(tr);
        });

    } catch (error) {
        tbody.innerHTML = `<tr><td colspan="5" class="text-center py-4 text-danger"><i class="fa-solid fa-triangle-exclamation me-2"></i>Failed to load history</td></tr>`;
        showErrorToast('Failed to load history');
    } finally {
        const btn = document.getElementById('refresh-history');
        btn.innerHTML = '<i class="fa-solid fa-rotate-right"></i> Refresh';
        btn.disabled = false;
    }
}

// ==========================================
// Utilities
// ==========================================

function showErrorToast(msg) {
    // Simple fallback since we don't have a toast container built in HTML
    console.error(msg);
    // In a real app, inject a Bootstrap toast here.
}
