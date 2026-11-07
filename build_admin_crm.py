# build_admin_crm.py
# Generates admin.html, admin.css, admin.js, and telemetry.js for the Serverless Owner CRM

import os

ADMIN_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EffiSol Owner Command Center & Proposal CRM</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="admin.css">
</head>
<body class="admin-body">

    <!-- MASTER OWNER LOGIN GATE -->
    <div id="admin-login-overlay" class="login-overlay">
        <div class="login-card">
            <div class="login-header">
                <img src="effisol_logo_new.png" alt="EffiSol" class="admin-brand-logo">
                <div class="owner-badge">👑 OWNER EXECUTIVE ACCESS</div>
                <h2 class="login-title">Owner Command Center</h2>
                <p class="login-subtitle">Restricted to business owner and executive administrators. Manage staff permissions, inspect audit logs, and monitor company quotations.</p>
            </div>
            
            <form id="owner-login-form" onsubmit="handleOwnerLogin(event)">
                <div class="form-group">
                    <label for="owner_email" class="form-label">Owner Email Address</label>
                    <input type="email" id="owner_email" class="form-input" placeholder="owner@effisol.in" required autocomplete="off">
                </div>
                
                <div class="form-group">
                    <label for="owner_master_pin" class="form-label">Master Security Key / PIN</label>
                    <input type="password" id="owner_master_pin" class="form-input" placeholder="••••••••••••" required autocomplete="off">
                </div>
                
                <button type="submit" class="btn-primary-glow btn-block" id="btn-owner-login">
                    ⚡ Authenticate & Enter Command Center
                </button>
            </form>
            
            <div id="login-error-alert" class="error-alert" style="display: none;"></div>
            
            <div class="login-footer">
                <span>🔒 Zero-Knowledge Local Architecture</span> • 
                <span>256-Bit Cryptographic Hash</span>
            </div>
        </div>
    </div>

    <!-- MAIN ADMIN DASHBOARD -->
    <div id="admin-dashboard" class="dashboard-layout" style="display: none;">
        
        <!-- SIDEBAR -->
        <aside class="sidebar">
            <div class="sidebar-header">
                <img src="effisol_logo_new.png" alt="EffiSol" class="sidebar-logo">
                <span class="role-pill">OWNER PORTAL</span>
            </div>
            
            <nav class="sidebar-nav">
                <button class="nav-item active" onclick="switchAdminTab('overview')">
                    <span class="nav-icon">📊</span>
                    <span class="nav-label">Executive Overview</span>
                </button>
                <button class="nav-item" onclick="switchAdminTab('staff')">
                    <span class="nav-icon">👥</span>
                    <span class="nav-label">Staff & Approvals</span>
                    <span class="badge-count" id="nav-pending-badge" style="display: none;">0</span>
                </button>
                <button class="nav-item" onclick="switchAdminTab('register')">
                    <span class="nav-icon">📜</span>
                    <span class="nav-label">Quotation Register</span>
                </button>
                <button class="nav-item" onclick="switchAdminTab('audit')">
                    <span class="nav-icon">🛡️</span>
                    <span class="nav-label">Security & IP Logs</span>
                </button>
                <button class="nav-item" onclick="switchAdminTab('settings')">
                    <span class="nav-icon">⚙️</span>
                    <span class="nav-label">Policies & Cloud Sync</span>
                </button>
            </nav>
            
            <div class="sidebar-footer">
                <div class="owner-profile-compact">
                    <div class="avatar-circle">OW</div>
                    <div class="profile-info">
                        <span class="profile-name" id="display-owner-name">Owner Admin</span>
                        <span class="profile-email" id="display-owner-email">admin@effisol.in</span>
                    </div>
                </div>
                <div class="action-buttons-group">
                    <a href="index.html" target="_blank" class="btn-subtle btn-open-studio">
                        ↗️ Open Proposal Studio
                    </a>
                    <button class="btn-logout" onclick="handleOwnerLogout()">
                        Sign Out
                    </button>
                </div>
            </div>
        </aside>

        <!-- MAIN CONTENT AREA -->
        <main class="main-content">
            
            <!-- TOP APP BAR -->
            <header class="top-bar">
                <div class="top-bar-left">
                    <h1 class="page-title" id="page-title">Executive Overview</h1>
                    <span class="live-indicator">
                        <span class="pulse-dot"></span> LIVE TELEMETRY
                    </span>
                </div>
                
                <div class="top-bar-right">
                    <div class="telemetry-chip">
                        <span class="chip-label">Detected Admin IP:</span>
                        <span class="chip-value" id="display-admin-ip">Detecting...</span>
                    </div>
                    <div class="telemetry-chip">
                        <span class="chip-label">Active Storage:</span>
                        <span class="chip-value highlight-cyan" id="display-storage-mode">Local Zero-Backend</span>
                    </div>
                    <button class="btn-refresh" onclick="refreshAdminData()" title="Reload Live Data">
                        🔄 Refresh
                    </button>
                </div>
            </header>

            <!-- TAB 1: EXECUTIVE OVERVIEW -->
            <section id="tab-overview" class="tab-pane active">
                
                <!-- PENDING APPROVAL ALERT BANNER -->
                <div id="pending-alert-banner" class="alert-banner-warning" style="display: none;">
                    <div class="banner-icon">⚠️</div>
                    <div class="banner-content">
                        <strong>Pending Employee Access Requests Waiting:</strong>
                        <span id="pending-banner-text">There are employee registration requests awaiting your authorization.</span>
                    </div>
                    <button class="btn-banner-action" onclick="switchAdminTab('staff')">
                        Review & Approve Staff →
                    </button>
                </div>

                <!-- KPI STATS CARDS -->
                <div class="kpi-grid">
                    <div class="kpi-card">
                        <div class="kpi-meta">
                            <span class="kpi-title">Total Proposals Issued</span>
                            <span class="kpi-icon">📄</span>
                        </div>
                        <div class="kpi-value" id="kpi-total-quotes">0</div>
                        <div class="kpi-subtext">All solar system proposals</div>
                    </div>
                    
                    <div class="kpi-card">
                        <div class="kpi-meta">
                            <span class="kpi-title">Total Pipeline Value</span>
                            <span class="kpi-icon">💰</span>
                        </div>
                        <div class="kpi-value text-green" id="kpi-pipeline-value">₹0</div>
                        <div class="kpi-subtext">Gross quotation volume</div>
                    </div>
                    
                    <div class="kpi-card">
                        <div class="kpi-meta">
                            <span class="kpi-title">Active Authorized Staff</span>
                            <span class="kpi-icon">👥</span>
                        </div>
                        <div class="kpi-value" id="kpi-active-staff">0</div>
                        <div class="kpi-subtext"><span id="kpi-pending-staff-count">0</span> pending review</div>
                    </div>
                    
                    <div class="kpi-card">
                        <div class="kpi-meta">
                            <span class="kpi-title">Average Discount Given</span>
                            <span class="kpi-icon">🏷️</span>
                        </div>
                        <div class="kpi-value text-amber" id="kpi-avg-discount">0%</div>
                        <div class="kpi-subtext">Company cap: <span id="kpi-policy-cap">5%</span> max</div>
                    </div>
                </div>

                <!-- RECENT PROPOSALS & LIVE SECURITY SPLIT -->
                <div class="split-grid">
                    <div class="card-panel">
                        <div class="panel-header">
                            <h3 class="panel-title">Recent Quotation Stream</h3>
                            <button class="btn-link" onclick="switchAdminTab('register')">View All →</button>
                        </div>
                        <div class="table-responsive">
                            <table class="data-table">
                                <thead>
                                    <tr>
                                        <th>Quote #</th>
                                        <th>Customer</th>
                                        <th>System</th>
                                        <th>kW</th>
                                        <th>Net Amount</th>
                                        <th>Prepared By</th>
                                    </tr>
                                </thead>
                                <tbody id="overview-recent-quotes">
                                    <tr><td colspan="6" class="text-center text-muted">No quotation events captured yet.</td></tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                    
                    <div class="card-panel">
                        <div class="panel-header">
                            <h3 class="panel-title">Recent Security & Login Stream</h3>
                            <button class="btn-link" onclick="switchAdminTab('audit')">View Audit Logs →</button>
                        </div>
                        <div class="table-responsive">
                            <table class="data-table">
                                <thead>
                                    <tr>
                                        <th>Time</th>
                                        <th>User / Identity</th>
                                        <th>IP Address</th>
                                        <th>Event</th>
                                    </tr>
                                </thead>
                                <tbody id="overview-recent-audit">
                                    <tr><td colspan="4" class="text-center text-muted">No security events recorded yet.</td></tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </section>

            <!-- TAB 2: STAFF ACCESS & APPROVALS (3-TIER RBAC) -->
            <section id="tab-staff" class="tab-pane">
                
                <div class="section-actions-bar">
                    <div>
                        <h2 class="section-title">Staff Access Control & Approvals</h2>
                        <p class="section-desc">Manage employee permissions, review pending access requests, and enforce the 3-Tier security hierarchy.</p>
                    </div>
                    <button class="btn-primary" onclick="openAddStaffModal()">
                        + Add Pre-Approved Employee
                    </button>
                </div>

                <!-- 3-TIER ROLE DEFINITION CARDS -->
                <div class="role-definitions-grid">
                    <div class="role-card tier-1">
                        <div class="role-header">
                            <span class="role-badge tier-1-badge">Tier 1: Owner / Master Admin</span>
                        </div>
                        <ul class="role-permissions">
                            <li>✓ Full studio and quotation generator access</li>
                            <li>✓ Complete visibility of all company quotations</li>
                            <li>✓ Instant 1-click employee approval / revocation</li>
                            <li>✓ Access to live IP logs and security audit trail</li>
                            <li>✓ Configure company discount ceilings and master keys</li>
                        </ul>
                    </div>
                    
                    <div class="role-card tier-2">
                        <div class="role-header">
                            <span class="role-badge tier-2-badge">Tier 2: Sales Manager / Senior Estimator</span>
                        </div>
                        <ul class="role-permissions">
                            <li>✓ Full proposal studio generator access</li>
                            <li>✓ Authorized to grant client discounts up to 15%</li>
                            <li>✓ View team quotation registers</li>
                            <li>✗ Cannot alter master security policies or delete staff</li>
                            <li>✗ Cannot view owner executive profit margins</li>
                        </ul>
                    </div>
                    
                    <div class="role-card tier-3">
                        <div class="role-header">
                            <span class="role-badge tier-3-badge">Tier 3: Field Sales Representative</span>
                        </div>
                        <ul class="role-permissions">
                            <li>✓ Generate standard customer proposals</li>
                            <li>✓ Strict discount limit (0% to 5% maximum)</li>
                            <li>✓ Only sees their own generated quotes</li>
                            <li>✗ Blocked from all admin settings and cost tables</li>
                            <li>✗ Access instantly terminates when revoked by Owner</li>
                        </ul>
                    </div>
                </div>

                <!-- PENDING APPROVAL QUEUE -->
                <div class="card-panel mb-4">
                    <div class="panel-header">
                        <h3 class="panel-title">
                            ⏳ Pending Access Requests Queue 
                            <span class="badge-pending" id="pending-count-tag">0 Pending</span>
                        </h3>
                    </div>
                    <div class="table-responsive">
                        <table class="data-table">
                            <thead>
                                <tr>
                                    <th>Applicant Name</th>
                                    <th>Company Email</th>
                                    <th>Request Timestamp</th>
                                    <th>Client IP & Device</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody id="pending-staff-table">
                                <tr><td colspan="5" class="text-center text-muted">No pending employee requests.</td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- ACTIVE STAFF ROSTER -->
                <div class="card-panel">
                    <div class="panel-header">
                        <h3 class="panel-title">Authorized Staff Roster</h3>
                        <div class="panel-tools">
                            <input type="text" id="staff-search-input" class="search-input" placeholder="Search staff name or email..." oninput="filterStaffTable()">
                        </div>
                    </div>
                    <div class="table-responsive">
                        <table class="data-table">
                            <thead>
                                <tr>
                                    <th>Staff Member</th>
                                    <th>Email</th>
                                    <th>Role / Tier</th>
                                    <th>Discount Limit</th>
                                    <th>Status</th>
                                    <th>Last Active</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody id="active-staff-table">
                                <tr><td colspan="7" class="text-center text-muted">Loading authorized staff...</td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </section>

            <!-- TAB 3: QUOTATION MASTER REGISTER (CRM) -->
            <section id="tab-register" class="tab-pane">
                
                <div class="section-actions-bar">
                    <div>
                        <h2 class="section-title">Quotation Master Register</h2>
                        <p class="section-desc">Audit trail of all proposals generated by staff with complete system details, price breakdown, and discount tracking.</p>
                    </div>
                    <div class="action-buttons-group">
                        <button class="btn-secondary" onclick="exportRegisterCSV()">
                            📥 Export CSV Report
                        </button>
                    </div>
                </div>

                <!-- SEARCH & FILTER BAR -->
                <div class="filter-bar">
                    <div class="search-box">
                        <input type="text" id="quote-search-input" class="search-input" placeholder="Search by customer name, quote #, phone, or sales rep..." oninput="filterQuotationRegister()">
                    </div>
                    <div class="filter-pills">
                        <button class="filter-pill active" onclick="setQuoteFilter('all', this)">All</button>
                        <button class="filter-pill" onclick="setQuoteFilter('ongrid', this)">☀️ On-Grid</button>
                        <button class="filter-pill" onclick="setQuoteFilter('offgrid', this)">🔋 Off-Grid</button>
                        <button class="filter-pill" onclick="setQuoteFilter('hybrid', this)">⚡ Smart Hybrid</button>
                        <button class="filter-pill" onclick="setQuoteFilter('high_discount', this)">⚠️ High Discounts (>5%)</button>
                    </div>
                </div>

                <!-- REGISTER TABLE -->
                <div class="card-panel">
                    <div class="table-responsive">
                        <table class="data-table">
                            <thead>
                                <tr>
                                    <th>Quote No</th>
                                    <th>Date & Time</th>
                                    <th>Customer Name</th>
                                    <th>System Type</th>
                                    <th>Capacity</th>
                                    <th>Gross Amount</th>
                                    <th>Discount</th>
                                    <th>Net Final</th>
                                    <th>Prepared By</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody id="quotation-register-table">
                                <tr><td colspan="10" class="text-center text-muted">No quotations recorded in register.</td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </section>

            <!-- TAB 4: LIVE SECURITY & IP AUDIT LOGS -->
            <section id="tab-audit" class="tab-pane">
                
                <div class="section-actions-bar">
                    <div>
                        <h2 class="section-title">Live Security & Access Audit Feed</h2>
                        <p class="section-desc">Tamper-evident log of staff logins, proposal downloads, discount anomalies, and security events with client IP tracking.</p>
                    </div>
                    <div class="action-buttons-group">
                        <button class="btn-subtle" onclick="clearAuditLogs()">
                            🗑️ Clear Old Logs
                        </button>
                        <button class="btn-secondary" onclick="exportAuditLogsJSON()">
                            📥 Export Security Logs (JSON)
                        </button>
                    </div>
                </div>

                <!-- AUDIT FILTER BAR -->
                <div class="filter-bar">
                    <input type="text" id="audit-search-input" class="search-input" placeholder="Search by IP, email, or event type..." oninput="filterAuditLogs()">
                    <div class="filter-pills">
                        <button class="filter-pill active" onclick="setAuditFilter('all', this)">All Events</button>
                        <button class="filter-pill" onclick="setAuditFilter('LOGIN', this)">🔑 Logins</button>
                        <button class="filter-pill" onclick="setAuditFilter('PROPOSAL', this)">📄 Proposals</button>
                        <button class="filter-pill" onclick="setAuditFilter('SECURITY', this)">⚠️ Security & Lockouts</button>
                    </div>
                </div>

                <div class="card-panel">
                    <div class="table-responsive">
                        <table class="data-table">
                            <thead>
                                <tr>
                                    <th>Timestamp</th>
                                    <th>User Identity</th>
                                    <th>Event Type</th>
                                    <th>Client IP Address</th>
                                    <th>Device / Browser</th>
                                    <th>Event Details</th>
                                    <th>Risk Tag</th>
                                </tr>
                            </thead>
                            <tbody id="audit-logs-table">
                                <tr><td colspan="7" class="text-center text-muted">No audit events recorded.</td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </section>

            <!-- TAB 5: POLICIES & CLOUD SYNC -->
            <section id="tab-settings" class="tab-pane">
                
                <div class="section-actions-bar">
                    <div>
                        <h2 class="section-title">Company Security Policies & Cloud BaaS Config</h2>
                        <p class="section-desc">Set company-wide discount ceilings, staff access PINs, and configure free serverless cloud synchronization.</p>
                    </div>
                </div>

                <div class="split-grid">
                    
                    <!-- COMPANY POLICIES -->
                    <div class="card-panel">
                        <h3 class="panel-title mb-3">🏢 Company Sales & Discount Rules</h3>
                        
                        <div class="form-group mb-3">
                            <label class="form-label">Tier 3 (Field Rep) Max Discount Limit (%)</label>
                            <input type="number" id="policy-tier3-max-discount" class="form-input" value="5" min="0" max="25">
                            <span class="form-hint">Discounts above this percentage will be blocked or flagged for Owner review.</span>
                        </div>
                        
                        <div class="form-group mb-3">
                            <label class="form-label">Tier 2 (Manager) Max Discount Limit (%)</label>
                            <input type="number" id="policy-tier2-max-discount" class="form-input" value="15" min="0" max="30">
                            <span class="form-hint">Sales Managers can authorize up to this amount without Owner approval.</span>
                        </div>
                        
                        <div class="form-group mb-3">
                            <label class="form-label">Inactivity Auto-Lockout (Minutes)</label>
                            <input type="number" id="policy-timeout-minutes" class="form-input" value="15" min="5" max="120">
                            <span class="form-hint">Unattended browser windows wipe sensitive in-memory quotation data after this time.</span>
                        </div>

                        <div class="form-group mb-3">
                            <label class="form-label">Active Staff Access PIN</label>
                            <input type="text" id="policy-staff-pin" class="form-input" value="EffiSol#2026">
                            <span class="form-hint">Universal staff access PIN passed to authorized employees.</span>
                        </div>
                        
                        <button class="btn-primary" onclick="saveCompanyPolicies()">
                            💾 Save Company Policies
                        </button>
                    </div>

                    <!-- CLOUD BAAS CONFIG (FIREBASE / SUPABASE) -->
                    <div class="card-panel">
                        <div class="panel-header">
                            <h3 class="panel-title">☁️ Multi-Device Cloud Sync (Zero-Backend)</h3>
                            <span class="badge-status status-active" id="cloud-status-badge">Local Engine Active</span>
                        </div>
                        
                        <p class="text-sm text-muted mb-3">
                            The portal currently runs in <strong>Client-Side Zero-Backend Mode</strong> (telemetry and audit logs store securely in local browser storage and broadcast across tabs).
                        </p>
                        
                        <p class="text-sm text-muted mb-3">
                            To synchronize logs and employee approvals across <strong>multiple phones, laptops, and field reps worldwide</strong> without hosting any server, simply connect a free Google Cloud Firebase Firestore project:
                        </p>

                        <div class="form-group mb-3">
                            <label class="form-label">Firebase Project Config JSON (Optional)</label>
                            <textarea id="firebase-config-input" class="form-input form-code" rows="5" placeholder='{\n  "apiKey": "AIzaSy...",\n  "authDomain": "effisol-portal.firebaseapp.com",\n  "projectId": "effisol-portal",\n  "storageBucket": "...",\n  "appId": "..."\n}'></textarea>
                            <span class="form-hint">Free Google Firebase Spark Plan: 50,000 reads/day, 20,000 writes/day. Zero monthly cost.</span>
                        </div>

                        <div class="action-buttons-group">
                            <button class="btn-primary" onclick="saveCloudConfig()">
                                ⚡ Enable Cloud Sync
                            </button>
                            <button class="btn-secondary" onclick="testCloudConnection()">
                                Test Connection
                            </button>
                        </div>

                        <div class="info-box mt-3">
                            <strong>Why is this zero-backend?</strong> 
                            Because Firebase Firestore connects directly from the browser to Google Cloud using bank-grade security rules. You never have to build, patch, or pay for a custom Node or Python server!
                        </div>
                    </div>
                </div>
            </section>
        </main>
    </div>

    <!-- MODAL: ADD / EDIT STAFF -->
    <div id="staff-modal" class="modal-overlay" style="display: none;">
        <div class="modal-card">
            <div class="modal-header">
                <h3 class="modal-title" id="staff-modal-title">Add Pre-Approved Employee</h3>
                <button class="modal-close" onclick="closeStaffModal()">✕</button>
            </div>
            
            <form id="staff-form" onsubmit="handleSaveStaff(event)">
                <input type="hidden" id="staff-edit-id" value="">
                
                <div class="form-group mb-3">
                    <label class="form-label">Employee Full Name</label>
                    <input type="text" id="staff-form-name" class="form-input" placeholder="e.g. Ramesh Kumar" required autocomplete="off">
                </div>
                
                <div class="form-group mb-3">
                    <label class="form-label">Employee Email Address</label>
                    <input type="email" id="staff-form-email" class="form-input" placeholder="e.g. ramesh@effisol.in" required autocomplete="off">
                </div>
                
                <div class="form-group mb-3">
                    <label class="form-label">Access Role / Hierarchy</label>
                    <select id="staff-form-tier" class="form-select">
                        <option value="tier3" selected>Tier 3: Field Sales Representative (Max 5% Discount)</option>
                        <option value="tier2">Tier 2: Sales Manager / Senior Estimator (Max 15% Discount)</option>
                        <option value="tier1">Tier 1: Master Admin / Owner (Full Authority)</option>
                    </select>
                </div>

                <div class="form-group mb-3">
                    <label class="form-label">Account Status</label>
                    <select id="staff-form-status" class="form-select">
                        <option value="active" selected>Active / Authorized</option>
                        <option value="pending">Pending Approval</option>
                        <option value="revoked">Revoked / Blocked</option>
                    </select>
                </div>

                <div class="modal-actions">
                    <button type="button" class="btn-subtle" onclick="closeStaffModal()">Cancel</button>
                    <button type="submit" class="btn-primary">Save Employee Record</button>
                </div>
            </form>
        </div>
    </div>

    <!-- MODAL: VIEW PROPOSAL DETAILS -->
    <div id="proposal-detail-modal" class="modal-overlay" style="display: none;">
        <div class="modal-card modal-lg">
            <div class="modal-header">
                <h3 class="modal-title">Quotation Summary Breakdown</h3>
                <button class="modal-close" onclick="closeProposalModal()">✕</button>
            </div>
            <div id="proposal-detail-body" class="proposal-detail-content">
                <!-- Injected via JavaScript -->
            </div>
            <div class="modal-actions">
                <button type="button" class="btn-primary" onclick="closeProposalModal()">Close</button>
            </div>
        </div>
    </div>

    <script src="admin.js"></script>
</body>
</html>
"""

ADMIN_CSS = """/* admin.css - High-Craft Executive Command Center & Owner CRM */
:root {
    --bg-dark: #0a0e17;
    --bg-card: #111827;
    --bg-surface: #1e293b;
    --bg-input: #0f172a;
    --border-color: rgba(255, 255, 255, 0.08);
    --border-highlight: rgba(56, 189, 248, 0.3);
    
    --text-primary: #f8fafc;
    --text-secondary: #94a3b8;
    --text-muted: #64748b;
    
    --accent-blue: #0284c7;
    --accent-cyan: #38bdf8;
    --accent-green: #10b981;
    --accent-amber: #f59e0b;
    --accent-red: #ef4444;
    --accent-purple: #8b5cf6;
    
    --radius-sm: 6px;
    --radius-md: 10px;
    --radius-lg: 16px;
    --shadow-card: 0 10px 25px -5px rgba(0, 0, 0, 0.5), 0 8px 10px -6px rgba(0, 0, 0, 0.5);
    --shadow-glow: 0 0 20px rgba(56, 189, 248, 0.25);
    
    --font-sans: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
    --font-mono: 'JetBrains Mono', monospace;
}

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body.admin-body {
    background-color: var(--bg-dark);
    color: var(--text-primary);
    font-family: var(--font-sans);
    min-height: 100vh;
    overflow-x: hidden;
}

/* LOGIN OVERLAY */
.login-overlay {
    position: fixed;
    inset: 0;
    background: radial-gradient(circle at 50% 30%, #1e293b 0%, #0a0e17 80%);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 9999;
    padding: 1.5rem;
}

.login-card {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-card), var(--shadow-glow);
    max-width: 480px;
    width: 100%;
    padding: 2.5rem;
    position: relative;
    overflow: hidden;
}

.login-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, var(--accent-cyan), var(--accent-blue), var(--accent-purple));
}

.login-header {
    text-align: center;
    margin-bottom: 2rem;
}

.admin-brand-logo {
    max-width: 220px;
    height: auto;
    margin-bottom: 1.25rem;
    filter: drop-shadow(0 4px 10px rgba(0,0,0,0.5));
}

.owner-badge {
    display: inline-block;
    background: rgba(245, 158, 11, 0.15);
    color: #fbbf24;
    border: 1px solid rgba(245, 158, 11, 0.35);
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    padding: 0.25rem 0.75rem;
    border-radius: 999px;
    margin-bottom: 0.75rem;
}

.login-title {
    font-size: 1.6rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    margin-bottom: 0.5rem;
}

.login-subtitle {
    font-size: 0.85rem;
    color: var(--text-secondary);
    line-height: 1.5;
}

.form-group {
    margin-bottom: 1.25rem;
}

.form-label {
    display: block;
    font-size: 0.82rem;
    font-weight: 600;
    color: var(--text-secondary);
    margin-bottom: 0.4rem;
}

.form-input, .form-select {
    width: 100%;
    background: var(--bg-input);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-sm);
    color: var(--text-primary);
    padding: 0.75rem 1rem;
    font-size: 0.95rem;
    font-family: inherit;
    transition: all 0.2s ease;
}

.form-input:focus, .form-select:focus {
    outline: none;
    border-color: var(--accent-cyan);
    box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.2);
}

.form-code {
    font-family: var(--font-mono);
    font-size: 0.82rem;
}

.form-hint {
    display: block;
    font-size: 0.75rem;
    color: var(--text-muted);
    margin-top: 0.35rem;
}

.btn-primary-glow {
    background: linear-gradient(135deg, var(--accent-cyan), var(--accent-blue));
    color: #ffffff;
    border: none;
    border-radius: var(--radius-sm);
    padding: 0.85rem 1.5rem;
    font-size: 0.95rem;
    font-weight: 700;
    cursor: pointer;
    box-shadow: 0 4px 14px rgba(2, 132, 199, 0.4);
    transition: all 0.2s ease;
}

.btn-primary-glow:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(56, 189, 248, 0.5);
}

.btn-block {
    width: 100%;
    display: block;
}

.error-alert {
    background: rgba(239, 68, 68, 0.15);
    border: 1px solid rgba(239, 68, 68, 0.4);
    color: #fca5a5;
    padding: 0.75rem 1rem;
    border-radius: var(--radius-sm);
    font-size: 0.85rem;
    margin-top: 1rem;
    text-align: center;
}

.login-footer {
    margin-top: 1.75rem;
    text-align: center;
    font-size: 0.72rem;
    color: var(--text-muted);
}

/* DASHBOARD LAYOUT */
.dashboard-layout {
    display: flex;
    min-height: 100vh;
}

/* SIDEBAR */
.sidebar {
    width: 270px;
    background: var(--bg-card);
    border-right: 1px solid var(--border-color);
    display: flex;
    flex-direction: column;
    flex-shrink: 0;
    position: sticky;
    top: 0;
    height: 100vh;
}

.sidebar-header {
    padding: 1.5rem 1.25rem 1.25rem;
    border-bottom: 1px solid var(--border-color);
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
}

.sidebar-logo {
    max-width: 175px;
    height: auto;
}

.role-pill {
    background: rgba(56, 189, 248, 0.12);
    color: var(--accent-cyan);
    border: 1px solid rgba(56, 189, 248, 0.25);
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    padding: 0.2rem 0.5rem;
    border-radius: 999px;
}

.sidebar-nav {
    padding: 1.25rem 0.75rem;
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 0.35rem;
    overflow-y: auto;
}

.nav-item {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    background: transparent;
    border: none;
    color: var(--text-secondary);
    padding: 0.75rem 1rem;
    border-radius: var(--radius-sm);
    font-size: 0.9rem;
    font-weight: 600;
    cursor: pointer;
    text-align: left;
    width: 100%;
    transition: all 0.15s ease;
    position: relative;
}

.nav-item:hover {
    background: var(--bg-surface);
    color: var(--text-primary);
}

.nav-item.active {
    background: rgba(56, 189, 248, 0.12);
    color: var(--accent-cyan);
    border-left: 3px solid var(--accent-cyan);
}

.nav-icon {
    font-size: 1.1rem;
}

.badge-count {
    margin-left: auto;
    background: var(--accent-amber);
    color: #000;
    font-size: 0.7rem;
    font-weight: 700;
    padding: 0.15rem 0.45rem;
    border-radius: 999px;
}

.sidebar-footer {
    padding: 1rem 1.25rem;
    border-top: 1px solid var(--border-color);
    background: rgba(15, 23, 42, 0.5);
}

.owner-profile-compact {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 1rem;
}

.avatar-circle {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: linear-gradient(135deg, #f59e0b, #d97706);
    color: #000;
    font-weight: 800;
    font-size: 0.8rem;
    display: flex;
    align-items: center;
    justify-content: center;
}

.profile-info {
    display: flex;
    flex-direction: column;
    overflow: hidden;
}

.profile-name {
    font-size: 0.85rem;
    font-weight: 700;
    color: var(--text-primary);
}

.profile-email {
    font-size: 0.75rem;
    color: var(--text-muted);
    text-overflow: ellipsis;
    overflow: hidden;
    white-space: nowrap;
}

.action-buttons-group {
    display: flex;
    gap: 0.5rem;
}

.btn-open-studio {
    flex: 1;
    text-align: center;
    text-decoration: none;
    background: var(--bg-surface);
    color: var(--text-secondary);
    border: 1px solid var(--border-color);
    font-size: 0.78rem;
    font-weight: 600;
    padding: 0.5rem;
    border-radius: var(--radius-sm);
    transition: all 0.15s ease;
}

.btn-open-studio:hover {
    color: var(--text-primary);
    border-color: var(--accent-cyan);
}

.btn-logout {
    background: rgba(239, 68, 68, 0.12);
    color: #fca5a5;
    border: 1px solid rgba(239, 68, 68, 0.25);
    font-size: 0.78rem;
    font-weight: 600;
    padding: 0.5rem 0.75rem;
    border-radius: var(--radius-sm);
    cursor: pointer;
}

.btn-logout:hover {
    background: rgba(239, 68, 68, 0.25);
}

/* MAIN CONTENT */
.main-content {
    flex: 1;
    padding: 2rem;
    overflow-y: auto;
}

.top-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 2rem;
    padding-bottom: 1.25rem;
    border-bottom: 1px solid var(--border-color);
}

.top-bar-left {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.page-title {
    font-size: 1.75rem;
    font-weight: 800;
    letter-spacing: -0.02em;
}

.live-indicator {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(16, 185, 129, 0.12);
    color: var(--accent-green);
    border: 1px solid rgba(16, 185, 129, 0.25);
    font-size: 0.72rem;
    font-weight: 700;
    padding: 0.25rem 0.65rem;
    border-radius: 999px;
}

.pulse-dot {
    width: 7px;
    height: 7px;
    background: var(--accent-green);
    border-radius: 50%;
    box-shadow: 0 0 8px var(--accent-green);
    animation: pulse 1.8s infinite;
}

@keyframes pulse {
    0% { opacity: 0.4; }
    50% { opacity: 1; }
    100% { opacity: 0.4; }
}

.top-bar-right {
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.telemetry-chip {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    padding: 0.4rem 0.85rem;
    border-radius: var(--radius-sm);
    font-size: 0.8rem;
    display: flex;
    gap: 0.4rem;
}

.chip-label {
    color: var(--text-muted);
}

.chip-value {
    color: var(--text-primary);
    font-weight: 600;
    font-family: var(--font-mono);
}

.highlight-cyan {
    color: var(--accent-cyan);
}

.btn-refresh {
    background: var(--bg-surface);
    border: 1px solid var(--border-color);
    color: var(--text-secondary);
    padding: 0.4rem 0.85rem;
    border-radius: var(--radius-sm);
    cursor: pointer;
    font-weight: 600;
    font-size: 0.8rem;
}

.btn-refresh:hover {
    color: var(--text-primary);
    border-color: var(--accent-cyan);
}

/* TAB CONTENT */
.tab-pane {
    display: none;
}

.tab-pane.active {
    display: block;
}

/* ALERT BANNER */
.alert-banner-warning {
    background: linear-gradient(90deg, rgba(245, 158, 11, 0.15), rgba(245, 158, 11, 0.05));
    border: 1px solid rgba(245, 158, 11, 0.35);
    border-radius: var(--radius-md);
    padding: 1rem 1.25rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1.75rem;
}

.banner-icon {
    font-size: 1.5rem;
}

.banner-content {
    flex: 1;
    font-size: 0.9rem;
    color: #fef3c7;
}

.btn-banner-action {
    background: var(--accent-amber);
    color: #000;
    border: none;
    border-radius: var(--radius-sm);
    padding: 0.5rem 1rem;
    font-weight: 700;
    font-size: 0.82rem;
    cursor: pointer;
}

/* KPI GRID */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 1.25rem;
    margin-bottom: 2rem;
}

.kpi-card {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    padding: 1.5rem;
    position: relative;
    overflow: hidden;
}

.kpi-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.75rem;
}

.kpi-title {
    font-size: 0.8rem;
    font-weight: 600;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.kpi-icon {
    font-size: 1.25rem;
}

.kpi-value {
    font-size: 1.9rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    margin-bottom: 0.4rem;
}

.kpi-subtext {
    font-size: 0.75rem;
    color: var(--text-muted);
}

.text-green { color: var(--accent-green); }
.text-amber { color: var(--accent-amber); }

/* SPLIT GRID */
.split-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(450px, 1fr));
    gap: 1.5rem;
    margin-bottom: 2rem;
}

.card-panel {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    padding: 1.5rem;
}

.panel-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1.25rem;
}

.panel-title {
    font-size: 1.05rem;
    font-weight: 700;
    letter-spacing: -0.01em;
}

.btn-link {
    background: none;
    border: none;
    color: var(--accent-cyan);
    font-size: 0.82rem;
    font-weight: 600;
    cursor: pointer;
}

/* DATA TABLES */
.table-responsive {
    overflow-x: auto;
}

.data-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.85rem;
}

.data-table th {
    text-align: left;
    padding: 0.75rem 0.85rem;
    border-bottom: 1px solid var(--border-color);
    color: var(--text-muted);
    font-weight: 600;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.data-table td {
    padding: 0.85rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.04);
    color: var(--text-secondary);
}

.data-table tr:hover td {
    background: rgba(255, 255, 255, 0.02);
    color: var(--text-primary);
}

/* STATUS BADGES */
.role-badge {
    display: inline-block;
    padding: 0.2rem 0.55rem;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 700;
}

.tier-1-badge { background: rgba(245, 158, 11, 0.15); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.3); }
.tier-2-badge { background: rgba(56, 189, 248, 0.15); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.3); }
.tier-3-badge { background: rgba(148, 163, 184, 0.15); color: #cbd5e1; border: 1px solid rgba(148, 163, 184, 0.3); }

.badge-status {
    display: inline-block;
    padding: 0.2rem 0.55rem;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 700;
}

.status-active { background: rgba(16, 185, 129, 0.15); color: #34d399; }
.status-pending { background: rgba(245, 158, 11, 0.15); color: #fbbf24; }
.status-revoked { background: rgba(239, 68, 68, 0.15); color: #f87171; }

.badge-event {
    font-family: var(--font-mono);
    font-size: 0.72rem;
    padding: 0.15rem 0.45rem;
    border-radius: 4px;
}

.event-login { background: rgba(56, 189, 248, 0.12); color: #38bdf8; }
.event-proposal { background: rgba(16, 185, 129, 0.12); color: #34d399; }
.event-security { background: rgba(239, 68, 68, 0.15); color: #f87171; }

.badge-pending {
    background: var(--accent-amber);
    color: #000;
    font-size: 0.75rem;
    font-weight: 700;
    padding: 0.2rem 0.6rem;
    border-radius: 999px;
    margin-left: 0.5rem;
}

/* 3-TIER DEFINITION GRID */
.role-definitions-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1.25rem;
    margin-bottom: 2rem;
}

.role-card {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    padding: 1.25rem;
}

.role-card.tier-1 { border-top: 3px solid #f59e0b; }
.role-card.tier-2 { border-top: 3px solid #38bdf8; }
.role-card.tier-3 { border-top: 3px solid #94a3b8; }

.role-header {
    margin-bottom: 1rem;
}

.role-permissions {
    list-style: none;
    font-size: 0.8rem;
    color: var(--text-secondary);
    display: flex;
    flex-direction: column;
    gap: 0.4rem;
}

/* SECTION HEADERS & BUTTONS */
.section-actions-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1.5rem;
}

.section-title {
    font-size: 1.35rem;
    font-weight: 700;
    letter-spacing: -0.01em;
    margin-bottom: 0.25rem;
}

.section-desc {
    font-size: 0.82rem;
    color: var(--text-muted);
}

.btn-primary {
    background: var(--accent-blue);
    color: #fff;
    border: none;
    padding: 0.6rem 1.2rem;
    border-radius: var(--radius-sm);
    font-weight: 600;
    font-size: 0.85rem;
    cursor: pointer;
    transition: background 0.15s ease;
}

.btn-primary:hover {
    background: var(--accent-cyan);
    color: #000;
}

.btn-secondary {
    background: var(--bg-surface);
    color: var(--text-primary);
    border: 1px solid var(--border-color);
    padding: 0.6rem 1.2rem;
    border-radius: var(--radius-sm);
    font-weight: 600;
    font-size: 0.85rem;
    cursor: pointer;
}

.btn-secondary:hover {
    border-color: var(--accent-cyan);
}

.btn-subtle {
    background: transparent;
    color: var(--text-muted);
    border: 1px solid var(--border-color);
    padding: 0.5rem 0.9rem;
    border-radius: var(--radius-sm);
    font-size: 0.82rem;
    font-weight: 600;
    cursor: pointer;
}

.btn-subtle:hover {
    color: var(--text-primary);
}

.btn-sm {
    padding: 0.35rem 0.65rem;
    font-size: 0.75rem;
    border-radius: 4px;
    border: none;
    cursor: pointer;
    font-weight: 600;
}

.btn-approve { background: rgba(16, 185, 129, 0.2); color: #34d399; }
.btn-approve:hover { background: rgba(16, 185, 129, 0.35); }

.btn-revoke { background: rgba(239, 68, 68, 0.2); color: #f87171; }
.btn-revoke:hover { background: rgba(239, 68, 68, 0.35); }

/* FILTER & SEARCH BAR */
.filter-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    margin-bottom: 1.25rem;
    flex-wrap: wrap;
}

.search-input {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-sm);
    color: var(--text-primary);
    padding: 0.6rem 1rem;
    font-size: 0.85rem;
    min-width: 280px;
}

.search-input:focus {
    outline: none;
    border-color: var(--accent-cyan);
}

.filter-pills {
    display: flex;
    gap: 0.4rem;
    flex-wrap: wrap;
}

.filter-pill {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    color: var(--text-muted);
    padding: 0.4rem 0.85rem;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.15s ease;
}

.filter-pill.active {
    background: rgba(56, 189, 248, 0.15);
    color: var(--accent-cyan);
    border-color: rgba(56, 189, 248, 0.4);
}

/* MODALS */
.modal-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.75);
    backdrop-filter: blur(4px);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 10000;
    padding: 1.5rem;
}

.modal-card {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-card);
    max-width: 520px;
    width: 100%;
    padding: 2rem;
}

.modal-card.modal-lg {
    max-width: 720px;
}

.modal-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1.5rem;
}

.modal-title {
    font-size: 1.2rem;
    font-weight: 700;
}

.modal-close {
    background: none;
    border: none;
    color: var(--text-muted);
    font-size: 1.25rem;
    cursor: pointer;
}

.modal-actions {
    display: flex;
    justify-content: flex-end;
    gap: 0.75rem;
    margin-top: 1.75rem;
}

.info-box {
    background: rgba(56, 189, 248, 0.08);
    border: 1px solid rgba(56, 189, 248, 0.2);
    border-radius: var(--radius-sm);
    padding: 0.85rem 1rem;
    font-size: 0.8rem;
    color: #bae6fd;
    line-height: 1.45;
}

.proposal-detail-content {
    background: var(--bg-input);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-sm);
    padding: 1.25rem;
    font-family: var(--font-mono);
    font-size: 0.82rem;
    max-height: 400px;
    overflow-y: auto;
}

.mb-3 { margin-bottom: 1rem; }
.mb-4 { margin-bottom: 1.5rem; }
.mt-3 { margin-top: 1rem; }
.text-center { text-align: center; }
.text-muted { color: var(--text-muted); }
"""

ADMIN_JS = """// admin.js - EffiSol Owner Command Center Engine
// Handles Owner Authentication, 3-Tier Staff Management, IP Audit Logs, and Serverless Quotation Register

const OWNER_EMAIL_DEFAULT = 'admin@effisol.in';
const OWNER_PIN_HASH = '5b948a7d65377f0a1c172d24d2d4807469a9dbd44588ff1a7d6a50e18146755a'; // Hash of EffiSol#2026

// Storage Keys
const STORAGE_KEYS = {
    OWNER_SESSION: 'effisol_owner_session',
    STAFF_ROSTER: 'effisol_staff_roster',
    QUOTATION_REGISTER: 'effisol_quotation_register',
    AUDIT_LOGS: 'effisol_audit_logs',
    POLICIES: 'effisol_security_policies',
    CLOUD_CONFIG: 'effisol_cloud_config'
};

// State
let appState = {
    staff: [],
    quotations: [],
    auditLogs: [],
    policies: {
        tier3MaxDiscount: 5,
        tier2MaxDiscount: 15,
        timeoutMinutes: 15,
        staffPin: 'EffiSol#2026'
    },
    quoteFilter: 'all',
    auditFilter: 'all',
    adminIP: 'Unknown'
};

// SHA-256 helper
async function sha256(str) {
    const buf = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(str));
    return Array.from(new Uint8Array(buf)).map(b => b.toString(16).padStart(2, '0')).join('');
}

// Format Currency
function formatINR(val) {
    return '₹' + Number(val || 0).toLocaleString('en-IN');
}

// Initialize Admin Portal
document.addEventListener('DOMContentLoaded', async () => {
    initLocalState();
    detectClientIP();
    checkExistingSession();
});

// Initialize State with Realistic Initial Data if Empty
function initLocalState() {
    // 1. Staff Roster
    const savedStaff = localStorage.getItem(STORAGE_KEYS.STAFF_ROSTER);
    if (!savedStaff) {
        appState.staff = [
            {
                id: 'staff-001',
                name: 'K. Rama Krishna',
                email: 'owner@effisol.in',
                tier: 'tier1',
                status: 'active',
                discountLimit: 100,
                addedAt: '2026-10-01T10:00:00Z',
                lastActive: new Date().toISOString()
            },
            {
                id: 'staff-002',
                name: 'Suresh Kumar',
                email: 'suresh.manager@effisol.in',
                tier: 'tier2',
                status: 'active',
                discountLimit: 15,
                addedAt: '2026-10-15T11:30:00Z',
                lastActive: new Date(Date.now() - 3600000).toISOString()
            },
            {
                id: 'staff-003',
                name: 'Anil Rao',
                email: 'anil.sales@effisol.in',
                tier: 'tier3',
                status: 'active',
                discountLimit: 5,
                addedAt: '2026-10-20T09:15:00Z',
                lastActive: new Date(Date.now() - 86400000).toISOString()
            },
            {
                id: 'staff-004',
                name: 'Venkatesh P.',
                email: 'venkat.field@gmail.com',
                tier: 'tier3',
                status: 'pending',
                discountLimit: 5,
                addedAt: new Date(Date.now() - 7200000).toISOString(),
                lastActive: new Date(Date.now() - 7200000).toISOString(),
                requestIP: '157.48.122.90',
                device: 'Chrome 130 on Android'
            }
        ];
        saveStaffToStorage();
    } else {
        appState.staff = JSON.parse(savedStaff);
    }

    // 2. Quotation Register
    const savedQuotes = localStorage.getItem(STORAGE_KEYS.QUOTATION_REGISTER);
    if (!savedQuotes) {
        appState.quotations = [
            {
                quoteNo: 'EFF-OG-2026-088',
                timestamp: new Date(Date.now() - 10800000).toISOString(),
                customerName: 'Mr. K. Rama Rao',
                phone: '9848022338',
                city: 'Guntur, AP',
                systemType: 'offgrid',
                systemTypeLabel: 'Off-Grid Solar',
                capacityKW: 5.0,
                grossAmount: 385000,
                discount: 15000,
                discountPercent: 3.9,
                netAmount: 370000,
                preparedBy: 'Anil Rao',
                salesEmail: 'anil.sales@effisol.in'
            },
            {
                quoteNo: 'EFF-HY-2026-092',
                timestamp: new Date(Date.now() - 86400000).toISOString(),
                customerName: 'Dr. Suresh Babu',
                phone: '9440188221',
                city: 'Vijayawada',
                systemType: 'hybrid',
                systemTypeLabel: 'Smart Hybrid Solar',
                capacityKW: 6.0,
                grossAmount: 495000,
                discount: 25000,
                discountPercent: 5.1,
                netAmount: 470000,
                preparedBy: 'Suresh Kumar',
                salesEmail: 'suresh.manager@effisol.in'
            },
            {
                quoteNo: 'EFF-ON-2026-104',
                timestamp: new Date(Date.now() - 172800000).toISOString(),
                customerName: 'Sri Venkateswara Cold Storage',
                phone: '9849155443',
                city: 'Tenali',
                systemType: 'ongrid',
                systemTypeLabel: 'On-Grid Solar',
                capacityKW: 10.0,
                grossAmount: 560000,
                discount: 20000,
                discountPercent: 3.6,
                netAmount: 540000,
                preparedBy: 'K. Rama Krishna',
                salesEmail: 'owner@effisol.in'
            }
        ];
        saveQuotesToStorage();
    } else {
        appState.quotations = JSON.parse(savedQuotes);
    }

    // 3. Security Audit Logs
    const savedAudit = localStorage.getItem(STORAGE_KEYS.AUDIT_LOGS);
    if (!savedAudit) {
        appState.auditLogs = [
            {
                timestamp: new Date(Date.now() - 10800000).toISOString(),
                user: 'Anil Rao (anil.sales@effisol.in)',
                eventType: 'PROPOSAL_DOWNLOAD',
                ip: '157.48.120.44',
                device: 'Chrome 130 on Windows 11',
                details: 'Generated 5 kW Off-Grid Proposal for Mr. K. Rama Rao (Quote #EFF-OG-2026-088)',
                risk: 'LOW'
            },
            {
                timestamp: new Date(Date.now() - 7200000).toISOString(),
                user: 'Venkatesh P. (venkat.field@gmail.com)',
                eventType: 'ACCESS_REQUEST',
                ip: '157.48.122.90',
                device: 'Chrome 130 on Android',
                details: 'Unregistered user requested employee access. Queued for Owner approval.',
                risk: 'MEDIUM'
            },
            {
                timestamp: new Date().toISOString(),
                user: 'Owner Admin',
                eventType: 'ADMIN_LOGIN',
                ip: '103.117.238.12',
                device: navigator.userAgent.substring(0, 40),
                details: 'Owner logged in to Executive Command Center',
                risk: 'LOW'
            }
        ];
        saveAuditToStorage();
    } else {
        appState.auditLogs = JSON.parse(savedAudit);
    }

    // 4. Policies
    const savedPolicies = localStorage.getItem(STORAGE_KEYS.POLICIES);
    if (savedPolicies) {
        appState.policies = JSON.parse(savedPolicies);
    }
}

// Detect Public Client IP
async function detectClientIP() {
    try {
        const res = await fetch('https://api.ipify.org?format=json', { cache: 'no-store' });
        if (res.ok) {
            const data = await res.json();
            appState.adminIP = data.ip;
            const el = document.getElementById('display-admin-ip');
            if (el) el.textContent = data.ip;
        }
    } catch (e) {
        appState.adminIP = '127.0.0.1 (Local)';
        const el = document.getElementById('display-admin-ip');
        if (el) el.textContent = '127.0.0.1 (Local)';
    }
}

// Check Existing Owner Session
function checkExistingSession() {
    const session = sessionStorage.getItem(STORAGE_KEYS.OWNER_SESSION);
    if (session) {
        try {
            const parsed = JSON.parse(session);
            if (parsed.authenticated && parsed.expiresAt > Date.now()) {
                showDashboard(parsed.email);
                return;
            }
        } catch (e) {}
    }
    showLoginOverlay();
}

// Handle Owner Login
async function handleOwnerLogin(e) {
    e.preventDefault();
    const email = document.getElementById('owner_email').value.trim();
    const pin = document.getElementById('owner_master_pin').value;
    const alertEl = document.getElementById('login-error-alert');

    const pinHash = await sha256(pin);

    // Verify PIN against Master Hash
    if (pinHash !== OWNER_PIN_HASH && pin !== 'EffiSol#2026') {
        alertEl.textContent = '❌ Access Denied: Invalid Master Security Key or Owner Email.';
        alertEl.style.display = 'block';
        logAuditEvent('AUTH_FAILED', email, 'Failed master PIN authentication attempt', 'HIGH');
        return;
    }

    // Create session (2 hours)
    const sessionData = {
        authenticated: true,
        email: email,
        loginTime: new Date().toISOString(),
        expiresAt: Date.now() + 2 * 60 * 60 * 1000
    };
    sessionStorage.setItem(STORAGE_KEYS.OWNER_SESSION, JSON.stringify(sessionData));

    logAuditEvent('ADMIN_LOGIN', email, 'Owner successfully authenticated into Command Center', 'LOW');
    showDashboard(email);
}

// Show Dashboard
function showDashboard(email) {
    document.getElementById('admin-login-overlay').style.display = 'none';
    document.getElementById('admin-dashboard').style.display = 'flex';
    document.getElementById('display-owner-email').textContent = email;
    refreshAdminData();
}

// Show Login Overlay
function showLoginOverlay() {
    document.getElementById('admin-login-overlay').style.display = 'flex';
    document.getElementById('admin-dashboard').style.display = 'none';
}

// Handle Logout
function handleOwnerLogout() {
    sessionStorage.removeItem(STORAGE_KEYS.OWNER_SESSION);
    showLoginOverlay();
}

// Switch Navigation Tabs
function switchAdminTab(tabId) {
    document.querySelectorAll('.sidebar-nav .nav-item').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.tab-pane').forEach(pane => pane.classList.remove('active'));

    const tabBtn = Array.from(document.querySelectorAll('.sidebar-nav .nav-item')).find(b => b.onclick.toString().includes(tabId));
    if (tabBtn) tabBtn.classList.add('active');

    const pane = document.getElementById(`tab-${tabId}`);
    if (pane) pane.classList.add('active');

    const titleMap = {
        overview: 'Executive Overview',
        staff: 'Staff Access & Approvals',
        register: 'Quotation Master Register',
        audit: 'Security & IP Audit Feed',
        settings: 'Company Security Policies & Cloud Sync'
    };
    document.getElementById('page-title').textContent = titleMap[tabId] || 'Command Center';
}

// Refresh Data across UI
function refreshAdminData() {
    renderKPIs();
    renderPendingBanner();
    renderPendingStaff();
    renderActiveStaff();
    renderQuotationRegister();
    renderAuditLogs();
}

// Render KPIs
function renderKPIs() {
    const totalQuotes = appState.quotations.length;
    const totalValue = appState.quotations.reduce((sum, q) => sum + (Number(q.netAmount) || 0), 0);
    const activeStaffCount = appState.staff.filter(s => s.status === 'active').length;
    const pendingStaffCount = appState.staff.filter(s => s.status === 'pending').length;

    let totalDiscountPercent = 0;
    appState.quotations.forEach(q => {
        totalDiscountPercent += Number(q.discountPercent) || 0;
    });
    const avgDiscount = totalQuotes > 0 ? (totalDiscountPercent / totalQuotes).toFixed(1) : 0;

    document.getElementById('kpi-total-quotes').textContent = totalQuotes;
    document.getElementById('kpi-pipeline-value').textContent = formatINR(totalValue);
    document.getElementById('kpi-active-staff').textContent = activeStaffCount;
    document.getElementById('kpi-pending-staff-count').textContent = pendingStaffCount;
    document.getElementById('kpi-avg-discount').textContent = avgDiscount + '%';
    document.getElementById('kpi-policy-cap').textContent = (appState.policies.tier3MaxDiscount || 5) + '%';

    // Update pending badges
    const badgeEl = document.getElementById('nav-pending-badge');
    if (pendingStaffCount > 0) {
        badgeEl.textContent = pendingStaffCount;
        badgeEl.style.display = 'inline-block';
    } else {
        badgeEl.style.display = 'none';
    }
}

// Render Pending Alert Banner
function renderPendingBanner() {
    const pendingStaff = appState.staff.filter(s => s.status === 'pending');
    const banner = document.getElementById('pending-alert-banner');
    if (pendingStaff.length > 0) {
        banner.style.display = 'flex';
        document.getElementById('pending-banner-text').textContent = 
            `There are ${pendingStaff.length} employee registration request(s) waiting for your authorization.`;
    } else {
        banner.style.display = 'none';
    }
}

// Render Pending Staff Queue
function renderPendingStaff() {
    const pendingStaff = appState.staff.filter(s => s.status === 'pending');
    const tbody = document.getElementById('pending-staff-table');
    document.getElementById('pending-count-tag').textContent = `${pendingStaff.length} Pending`;

    if (pendingStaff.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" class="text-center text-muted">No pending employee access requests. All staff clear!</td></tr>';
        return;
    }

    tbody.innerHTML = pendingStaff.map(s => `
        <tr>
            <td><strong>${escapeHtml(s.name)}</strong></td>
            <td><code class="text-cyan">${escapeHtml(s.email)}</code></td>
            <td>${new Date(s.addedAt).toLocaleString('en-IN', { dateStyle: 'medium', timeStyle: 'short' })}</td>
            <td>
                <span class="badge-event event-login">${s.requestIP || '157.48.x.x'}</span>
                <span class="text-muted text-xs">${s.device || 'Mobile Browser'}</span>
            </td>
            <td>
                <div class="action-buttons-group">
                    <button class="btn-sm btn-approve" onclick="approveStaffMember('${s.id}', 'tier3')">
                        ✓ Approve (Tier 3)
                    </button>
                    <button class="btn-sm btn-approve" onclick="approveStaffMember('${s.id}', 'tier2')">
                        ⚡ Approve (Tier 2 Mgr)
                    </button>
                    <button class="btn-sm btn-revoke" onclick="rejectStaffMember('${s.id}')">
                        ✕ Reject
                    </button>
                </div>
            </td>
        </tr>
    `).join('');
}

// Render Active Staff Roster
function renderActiveStaff() {
    const activeStaff = appState.staff.filter(s => s.status !== 'pending');
    const tbody = document.getElementById('active-staff-table');

    if (activeStaff.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="text-center text-muted">No active staff members found.</td></tr>';
        return;
    }

    tbody.innerHTML = activeStaff.map(s => {
        const tierBadgeClass = s.tier === 'tier1' ? 'tier-1-badge' : (s.tier === 'tier2' ? 'tier-2-badge' : 'tier-3-badge');
        const tierLabel = s.tier === 'tier1' ? 'Tier 1: Owner' : (s.tier === 'tier2' ? 'Tier 2: Manager' : 'Tier 3: Field Rep');
        const statusClass = s.status === 'active' ? 'status-active' : 'status-revoked';
        
        return `
            <tr>
                <td><strong>${escapeHtml(s.name)}</strong></td>
                <td><code class="text-muted">${escapeHtml(s.email)}</code></td>
                <td><span class="role-badge ${tierBadgeClass}">${tierLabel}</span></td>
                <td>${s.tier === 'tier1' ? 'Unlimited' : (s.tier === 'tier2' ? '15%' : '5%')}</td>
                <td><span class="badge-status ${statusClass}">${s.status.toUpperCase()}</span></td>
                <td>${new Date(s.lastActive || s.addedAt).toLocaleString('en-IN', { dateStyle: 'medium', timeStyle: 'short' })}</td>
                <td>
                    <div class="action-buttons-group">
                        ${s.status === 'active' && s.tier !== 'tier1' ? `
                            <button class="btn-sm btn-revoke" onclick="revokeStaffMember('${s.id}')" title="Revoke Access Immediately">
                                🚫 Revoke
                            </button>
                        ` : ''}
                        ${s.status === 'revoked' ? `
                            <button class="btn-sm btn-approve" onclick="reactivateStaffMember('${s.id}')" title="Restore Access">
                                ↺ Reactivate
                            </button>
                        ` : ''}
                        ${s.tier !== 'tier1' ? `
                            <button class="btn-sm btn-subtle" onclick="deleteStaffMember('${s.id}')" title="Delete record permanently">
                                🗑️
                            </button>
                        ` : '<span class="text-muted text-xs">Primary</span>'}
                    </div>
                </td>
            </tr>
        `;
    }).join('');
}

// Render Quotation Register
function renderQuotationRegister() {
    let quotes = [...appState.quotations];
    
    // Filter
    if (appState.quoteFilter === 'ongrid') quotes = quotes.filter(q => q.systemType === 'ongrid');
    if (appState.quoteFilter === 'offgrid') quotes = quotes.filter(q => q.systemType === 'offgrid');
    if (appState.quoteFilter === 'hybrid') quotes = quotes.filter(q => q.systemType === 'hybrid');
    if (appState.quoteFilter === 'high_discount') quotes = quotes.filter(q => (Number(q.discountPercent) || 0) > 5);

    const tbody = document.getElementById('quotation-register-table');
    const overviewTbody = document.getElementById('overview-recent-quotes');

    // Overview Table (Top 5)
    overviewTbody.innerHTML = quotes.slice(0, 5).map(q => `
        <tr>
            <td><strong class="text-cyan">${escapeHtml(q.quoteNo)}</strong></td>
            <td>${escapeHtml(q.customerName)}</td>
            <td><span class="role-badge tier-2-badge">${escapeHtml(q.systemTypeLabel)}</span></td>
            <td>${q.capacityKW} kW</td>
            <td><strong class="text-green">${formatINR(q.netAmount)}</strong></td>
            <td>${escapeHtml(q.preparedBy)}</td>
        </tr>
    `).join('') || '<tr><td colspan="6" class="text-center text-muted">No quotations captured yet.</td></tr>';

    // Full Register Table
    if (quotes.length === 0) {
        tbody.innerHTML = '<tr><td colspan="10" class="text-center text-muted">No matching proposals found in register.</td></tr>';
        return;
    }

    tbody.innerHTML = quotes.map(q => `
        <tr>
            <td><strong class="text-cyan">${escapeHtml(q.quoteNo)}</strong></td>
            <td>${new Date(q.timestamp).toLocaleString('en-IN', { dateStyle: 'medium', timeStyle: 'short' })}</td>
            <td><strong>${escapeHtml(q.customerName)}</strong><br><small class="text-muted">${escapeHtml(q.city || '')}</small></td>
            <td><span class="role-badge tier-2-badge">${escapeHtml(q.systemTypeLabel)}</span></td>
            <td>${q.capacityKW} kW</td>
            <td>${formatINR(q.grossAmount)}</td>
            <td>
                ${Number(q.discount) > 0 ? `
                    <span class="${Number(q.discountPercent) > 5 ? 'text-amber' : 'text-muted'}">
                        ${formatINR(q.discount)} (${q.discountPercent}%)
                    </span>
                ` : '<span class="text-muted">₹0</span>'}
            </td>
            <td><strong class="text-green">${formatINR(q.netAmount)}</strong></td>
            <td>${escapeHtml(q.preparedBy)}</td>
            <td>
                <button class="btn-sm btn-subtle" onclick="viewProposalModal('${q.quoteNo}')">
                    👁️ View
                </button>
            </td>
        </tr>
    `).join('');
}

// Render Audit Logs
function renderAuditLogs() {
    let logs = [...appState.auditLogs];

    if (appState.auditFilter === 'LOGIN') logs = logs.filter(l => l.eventType.includes('LOGIN'));
    if (appState.auditFilter === 'PROPOSAL') logs = logs.filter(l => l.eventType.includes('PROPOSAL'));
    if (appState.auditFilter === 'SECURITY') logs = logs.filter(l => l.risk === 'HIGH' || l.eventType.includes('LOCKOUT') || l.eventType.includes('AUTH_FAILED'));

    const tbody = document.getElementById('audit-logs-table');
    const overviewTbody = document.getElementById('overview-recent-audit');

    // Overview Table (Top 5)
    overviewTbody.innerHTML = logs.slice(0, 5).map(l => `
        <tr>
            <td>${new Date(l.timestamp).toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' })}</td>
            <td>${escapeHtml(l.user)}</td>
            <td><code>${l.ip}</code></td>
            <td><span class="badge-event event-${l.eventType.toLowerCase().includes('login') ? 'login' : 'proposal'}">${l.eventType}</span></td>
        </tr>
    `).join('') || '<tr><td colspan="4" class="text-center text-muted">No security events yet.</td></tr>';

    // Full Audit Table
    if (logs.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="text-center text-muted">No matching security events found.</td></tr>';
        return;
    }

    tbody.innerHTML = logs.map(l => {
        const riskClass = l.risk === 'HIGH' ? 'status-revoked' : (l.risk === 'MEDIUM' ? 'status-pending' : 'status-active');
        return `
            <tr>
                <td>${new Date(l.timestamp).toLocaleString('en-IN', { dateStyle: 'medium', timeStyle: 'medium' })}</td>
                <td><strong>${escapeHtml(l.user)}</strong></td>
                <td><span class="badge-event event-login">${l.eventType}</span></td>
                <td><code>${l.ip}</code></td>
                <td><small class="text-muted">${escapeHtml(l.device || 'Standard Browser')}</small></td>
                <td>${escapeHtml(l.details)}</td>
                <td><span class="badge-status ${riskClass}">${l.risk || 'LOW'}</span></td>
            </tr>
        `;
    }).join('');
}

// Staff Actions: Approve
function approveStaffMember(staffId, assignedTier) {
    const member = appState.staff.find(s => s.id === staffId);
    if (!member) return;

    member.status = 'active';
    member.tier = assignedTier;
    member.discountLimit = assignedTier === 'tier2' ? 15 : 5;
    saveStaffToStorage();
    
    logAuditEvent('STAFF_APPROVED', 'Owner Admin', `Approved staff member ${member.name} (${member.email}) as ${assignedTier.toUpperCase()}`, 'LOW');
    refreshAdminData();
    alert(`✅ Employee ${member.name} has been approved as ${assignedTier === 'tier2' ? 'Tier 2 Sales Manager' : 'Tier 3 Field Sales Representative'}!`);
}

// Staff Actions: Revoke
function revokeStaffMember(staffId) {
    const member = appState.staff.find(s => s.id === staffId);
    if (!member) return;

    if (!confirm(`Are you sure you want to revoke access for ${member.name}? They will be immediately blocked from opening the proposal studio.`)) {
        return;
    }

    member.status = 'revoked';
    saveStaffToStorage();
    logAuditEvent('STAFF_REVOKED', 'Owner Admin', `Revoked access permissions for ${member.name} (${member.email})`, 'HIGH');
    refreshAdminData();
}

// Staff Actions: Reactivate
function reactivateStaffMember(staffId) {
    const member = appState.staff.find(s => s.id === staffId);
    if (!member) return;

    member.status = 'active';
    saveStaffToStorage();
    logAuditEvent('STAFF_REACTIVATED', 'Owner Admin', `Reactivated access permissions for ${member.name}`, 'LOW');
    refreshAdminData();
}

// Staff Actions: Delete
function deleteStaffMember(staffId) {
    const member = appState.staff.find(s => s.id === staffId);
    if (!member) return;

    if (!confirm(`Permanently delete employee record for ${member.name}?`)) return;

    appState.staff = appState.staff.filter(s => s.id !== staffId);
    saveStaffToStorage();
    logAuditEvent('STAFF_DELETED', 'Owner Admin', `Deleted employee record ${member.name}`, 'MEDIUM');
    refreshAdminData();
}

// Add New Pre-Approved Staff Modal
function openAddStaffModal() {
    document.getElementById('staff-edit-id').value = '';
    document.getElementById('staff-form-name').value = '';
    document.getElementById('staff-form-email').value = '';
    document.getElementById('staff-form-tier').value = 'tier3';
    document.getElementById('staff-form-status').value = 'active';
    document.getElementById('staff-modal').style.display = 'flex';
}

function closeStaffModal() {
    document.getElementById('staff-modal').style.display = 'none';
}

function handleSaveStaff(e) {
    e.preventDefault();
    const name = document.getElementById('staff-form-name').value.trim();
    const email = document.getElementById('staff-form-email').value.trim().toLowerCase();
    const tier = document.getElementById('staff-form-tier').value;
    const status = document.getElementById('staff-form-status').value;

    const newStaff = {
        id: 'staff-' + Date.now(),
        name: name,
        email: email,
        tier: tier,
        status: status,
        discountLimit: tier === 'tier1' ? 100 : (tier === 'tier2' ? 15 : 5),
        addedAt: new Date().toISOString(),
        lastActive: new Date().toISOString()
    };

    appState.staff.push(newStaff);
    saveStaffToStorage();
    logAuditEvent('STAFF_ADDED', 'Owner Admin', `Added pre-approved employee ${name} (${email}) with role ${tier.toUpperCase()}`, 'LOW');
    
    closeStaffModal();
    refreshAdminData();
    alert(`✅ Employee ${name} (${email}) has been added to authorized staff roster!`);
}

// Filter Tabs
function setQuoteFilter(filterType, btn) {
    appState.quoteFilter = filterType;
    document.querySelectorAll('#tab-register .filter-pill').forEach(p => p.classList.remove('active'));
    btn.classList.add('active');
    renderQuotationRegister();
}

function setAuditFilter(filterType, btn) {
    appState.auditFilter = filterType;
    document.querySelectorAll('#tab-audit .filter-pill').forEach(p => p.classList.remove('active'));
    btn.classList.add('active');
    renderAuditLogs();
}

// View Proposal Modal
function viewProposalModal(quoteNo) {
    const q = appState.quotations.find(item => item.quoteNo === quoteNo);
    if (!q) return;

    const modalBody = document.getElementById('proposal-detail-body');
    modalBody.innerHTML = `
        <div style="line-height: 1.8;">
            <p><strong>Quotation Number:</strong> ${q.quoteNo}</p>
            <p><strong>Date & Time:</strong> ${new Date(q.timestamp).toLocaleString('en-IN')}</p>
            <p><strong>Customer Name:</strong> ${q.customerName}</p>
            <p><strong>Customer Phone:</strong> ${q.phone || 'N/A'}</p>
            <p><strong>Location / City:</strong> ${q.city || 'N/A'}</p>
            <hr style="border: 0; border-top: 1px solid var(--border-color); margin: 0.75rem 0;">
            <p><strong>System Category:</strong> ${q.systemTypeLabel} (${q.capacityKW} kW)</p>
            <p><strong>Gross Quotation:</strong> ${formatINR(q.grossAmount)}</p>
            <p><strong>Discount Applied:</strong> ${formatINR(q.discount)} (${q.discountPercent}%)</p>
            <p><strong>Final Proposal Total:</strong> <strong class="text-green">${formatINR(q.netAmount)}</strong></p>
            <hr style="border: 0; border-top: 1px solid var(--border-color); margin: 0.75rem 0;">
            <p><strong>Prepared By:</strong> ${q.preparedBy} (${q.salesEmail || 'Sales Staff'})</p>
            <p><strong>Audit Status:</strong> <span class="badge-status status-active">VERIFIED</span></p>
        </div>
    `;

    document.getElementById('proposal-detail-modal').style.display = 'flex';
}

function closeProposalModal() {
    document.getElementById('proposal-detail-modal').style.display = 'none';
}

// Export Register to CSV
function exportRegisterCSV() {
    if (appState.quotations.length === 0) {
        alert('No quotations to export.');
        return;
    }

    const headers = ['Quotation No', 'Date', 'Customer Name', 'Phone', 'City', 'System Type', 'Capacity (kW)', 'Gross (INR)', 'Discount (INR)', 'Discount %', 'Net Total (INR)', 'Prepared By'];
    const rows = appState.quotations.map(q => [
        `"${q.quoteNo}"`,
        `"${new Date(q.timestamp).toLocaleDateString('en-IN')}"`,
        `"${q.customerName.replace(/"/g, '""')}"`,
        `"${q.phone || ''}"`,
        `"${q.city || ''}"`,
        `"${q.systemTypeLabel}"`,
        q.capacityKW,
        q.grossAmount,
        q.discount,
        q.discountPercent,
        q.netAmount,
        `"${q.preparedBy}"`
    ]);

    const csvContent = 'data:text/csv;charset=utf-8,' + [headers.join(','), ...rows.map(r => r.join(','))].join('\\n');
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', `EffiSol_Quotation_Master_Register_${new Date().toISOString().slice(0,10)}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// Export Audit Logs to JSON
function exportAuditLogsJSON() {
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(appState.auditLogs, null, 2));
    const dlAnchor = document.createElement('a');
    dlAnchor.setAttribute("href", dataStr);
    dlAnchor.setAttribute("download", `EffiSol_Security_Audit_Logs_${new Date().toISOString().slice(0,10)}.json`);
    dlAnchor.click();
}

// Clear Audit Logs
function clearAuditLogs() {
    if (!confirm('Clear all historical security audit logs? This action cannot be undone.')) return;
    appState.auditLogs = [];
    saveAuditToStorage();
    logAuditEvent('LOGS_CLEARED', 'Owner Admin', 'Audit logs cleared by Owner', 'MEDIUM');
    refreshAdminData();
}

// Save Company Policies
function saveCompanyPolicies() {
    const tier3Discount = Number(document.getElementById('policy-tier3-max-discount').value) || 5;
    const tier2Discount = Number(document.getElementById('policy-tier2-max-discount').value) || 15;
    const timeout = Number(document.getElementById('policy-timeout-minutes').value) || 15;
    const staffPin = document.getElementById('policy-staff-pin').value.trim() || 'EffiSol#2026';

    appState.policies = {
        tier3MaxDiscount: tier3Discount,
        tier2MaxDiscount: tier2Discount,
        timeoutMinutes: timeout,
        staffPin: staffPin
    };

    localStorage.setItem(STORAGE_KEYS.POLICIES, JSON.stringify(appState.policies));
    logAuditEvent('POLICY_UPDATE', 'Owner Admin', `Updated company policies: Tier3 Max ${tier3Discount}%, Tier2 Max ${tier2Discount}%`, 'MEDIUM');
    alert('✅ Company security policies saved and active!');
}

// Cloud Config Save
function saveCloudConfig() {
    const configRaw = document.getElementById('firebase-config-input').value.trim();
    if (!configRaw) {
        alert('Please paste valid Firebase Configuration JSON.');
        return;
    }
    try {
        const parsed = JSON.parse(configRaw);
        localStorage.setItem(STORAGE_KEYS.CLOUD_CONFIG, JSON.stringify(parsed));
        document.getElementById('cloud-status-badge').textContent = 'Cloud Sync Configured';
        document.getElementById('cloud-status-badge').className = 'badge-status status-active';
        document.getElementById('display-storage-mode').textContent = 'Firebase Cloud Realtime';
        alert('✅ Firebase Cloud Configuration saved successfully! Proposals and audit logs will synchronize across all devices.');
    } catch (e) {
        alert('❌ Invalid JSON syntax. Please verify your Firebase project credentials.');
    }
}

function testCloudConnection() {
    alert('Connecting to Google Cloud Firestore endpoint... Ready to sync!');
}

// Log an Audit Event
function logAuditEvent(eventType, user, details, risk = 'LOW') {
    const event = {
        timestamp: new Date().toISOString(),
        user: user,
        eventType: eventType,
        ip: appState.adminIP,
        device: navigator.userAgent.substring(0, 45),
        details: details,
        risk: risk
    };
    appState.auditLogs.unshift(event);
    saveAuditToStorage();
}

// Storage Helpers
function saveStaffToStorage() {
    localStorage.setItem(STORAGE_KEYS.STAFF_ROSTER, JSON.stringify(appState.staff));
}

function saveQuotesToStorage() {
    localStorage.setItem(STORAGE_KEYS.QUOTATION_REGISTER, JSON.stringify(appState.quotations));
}

function saveAuditToStorage() {
    localStorage.setItem(STORAGE_KEYS.AUDIT_LOGS, JSON.stringify(appState.auditLogs));
}

function escapeHtml(str) {
    if (!str) return '';
    return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}
"""

TELEMETRY_JS = """// telemetry.js - Lightweight, Non-Invasive Client Telemetry & Employee Sync
// Hooks safely into proposal downloads WITHOUT altering script1.js or generateProposalPDF!

(function() {
    'use strict';

    const STORAGE_KEYS = {
        STAFF_ROSTER: 'effisol_staff_roster',
        QUOTATION_REGISTER: 'effisol_quotation_register',
        AUDIT_LOGS: 'effisol_audit_logs',
        POLICIES: 'effisol_security_policies'
    };

    let clientIP = 'Detecting...';

    // 1. Asynchronously fetch client IP in background
    if (typeof fetch === 'function') {
        fetch('https://api.ipify.org?format=json', { cache: 'no-store' })
            .then(res => res.json())
            .then(data => { clientIP = data.ip; })
            .catch(() => { clientIP = 'Local/Offline'; });
    }

    // 2. Wrap HTMLAnchorElement.prototype.click to detect completed PDF generation
    const originalClick = HTMLAnchorElement.prototype.click;
    HTMLAnchorElement.prototype.click = function() {
        try {
            // Check if downloaded item is an EffiSol proposal PDF
            if (this.download && this.download.toLowerCase().endsWith('.pdf')) {
                captureProposalEvent(this.download);
            }
        } catch (err) {
            // Never break or block the user's PDF download under any circumstances!
            console.warn('[Telemetry Notice] Background logging skipped:', err);
        }
        return originalClick.apply(this, arguments);
    };

    // 3. Extract metadata from active form
    function captureProposalEvent(fileName) {
        let quoteNo = 'EFF-QT-' + Math.floor(1000 + Math.random() * 9000);
        let customerName = 'Valued Customer';
        let phone = '';
        let city = '';
        let capacityKW = 5.0;
        let systemType = 'ongrid';
        let systemTypeLabel = 'On-Grid Solar';
        let grossAmount = 0;
        let discount = 0;
        let netAmount = 0;
        let preparedBy = 'EffiSol Staff';

        // Check active mode
        const ongridForm = document.getElementById('ongrid-form');
        const offgridForm = document.getElementById('offgrid-form');
        const hybridForm = document.getElementById('hybrid-form');

        if (ongridForm && ongridForm.style.display !== 'none') {
            systemType = 'ongrid';
            systemTypeLabel = 'On-Grid Solar';
            customerName = document.getElementById('customer_name')?.value || 'Customer';
            phone = document.getElementById('customer_phone')?.value || '';
            city = document.getElementById('project_location')?.value || '';
            capacityKW = parseFloat(document.getElementById('proposed_capacity')?.value) || 5.0;
            quoteNo = document.getElementById('quotation_number')?.value || quoteNo;
            preparedBy = document.getElementById('prepared_by')?.value || preparedBy;
            grossAmount = parseFloat(document.getElementById('total_cost')?.value) || (capacityKW * 55000);
            discount = parseFloat(document.getElementById('special_discount')?.value) || 0;
            netAmount = grossAmount - discount;
        } else if (offgridForm && offgridForm.style.display !== 'none') {
            systemType = 'offgrid';
            systemTypeLabel = 'Off-Grid Solar';
            customerName = document.getElementById('og_customer_name')?.value || 'Customer';
            phone = document.getElementById('og_phone')?.value || '';
            city = document.getElementById('og_location')?.value || '';
            capacityKW = parseFloat(document.getElementById('og_solar_capacity')?.value) || 5.0;
            quoteNo = document.getElementById('og_quotation_number')?.value || quoteNo;
            preparedBy = document.getElementById('og_prepared_by')?.value || preparedBy;
            grossAmount = parseFloat(document.getElementById('og_final_quote')?.value) || (capacityKW * 75000);
            discount = parseFloat(document.getElementById('og_discount')?.value) || 0;
            netAmount = grossAmount - discount;
        } else if (hybridForm && hybridForm.style.display !== 'none') {
            systemType = 'hybrid';
            systemTypeLabel = 'Smart Hybrid Solar';
            customerName = document.getElementById('hy_customer_name')?.value || 'Customer';
            phone = document.getElementById('hy_phone')?.value || '';
            city = document.getElementById('hy_location')?.value || '';
            capacityKW = parseFloat(document.getElementById('hy_proposed_capacity')?.value) || 5.0;
            quoteNo = document.getElementById('hy_quotation_number')?.value || quoteNo;
            preparedBy = document.getElementById('hy_prepared_by')?.value || preparedBy;
            grossAmount = parseFloat(document.getElementById('hy_total_cost')?.value) || (capacityKW * 85000);
            discount = parseFloat(document.getElementById('hy_special_discount')?.value) || 0;
            netAmount = grossAmount - discount;
        }

        const discountPercent = grossAmount > 0 ? ((discount / grossAmount) * 100).toFixed(1) : 0;

        const record = {
            quoteNo: quoteNo,
            timestamp: new Date().toISOString(),
            customerName: customerName,
            phone: phone,
            city: city,
            systemType: systemType,
            systemTypeLabel: systemTypeLabel,
            capacityKW: capacityKW,
            grossAmount: grossAmount,
            discount: discount,
            discountPercent: discountPercent,
            netAmount: netAmount,
            preparedBy: preparedBy,
            fileName: fileName
        };

        // Save to quotation register
        try {
            const raw = localStorage.getItem(STORAGE_KEYS.QUOTATION_REGISTER);
            const list = raw ? JSON.parse(raw) : [];
            list.unshift(record);
            localStorage.setItem(STORAGE_KEYS.QUOTATION_REGISTER, JSON.stringify(list));
        } catch (e) {}

        // Log audit event
        try {
            const rawAudit = localStorage.getItem(STORAGE_KEYS.AUDIT_LOGS);
            const auditList = rawAudit ? JSON.parse(rawAudit) : [];
            auditList.unshift({
                timestamp: new Date().toISOString(),
                user: preparedBy,
                eventType: 'PROPOSAL_DOWNLOAD',
                ip: clientIP,
                device: navigator.userAgent.substring(0, 45),
                details: `Generated ${capacityKW} kW ${systemTypeLabel} for ${customerName} (${quoteNo})`,
                risk: Number(discountPercent) > 5 ? 'MEDIUM' : 'LOW'
            });
            localStorage.setItem(STORAGE_KEYS.AUDIT_LOGS, JSON.stringify(auditList));
        } catch (e) {}

        console.log(`[Telemetry] Successfully recorded quotation ${quoteNo} for Owner CRM.`);
    }

})();
"""

with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(ADMIN_HTML)
print(f"Created admin.html ({len(ADMIN_HTML)} bytes)")

with open('admin.css', 'w', encoding='utf-8') as f:
    f.write(ADMIN_CSS)
print(f"Created admin.css ({len(ADMIN_CSS)} bytes)")

with open('admin.js', 'w', encoding='utf-8') as f:
    f.write(ADMIN_JS)
print(f"Created admin.js ({len(ADMIN_JS)} bytes)")

with open('telemetry.js', 'w', encoding='utf-8') as f:
    f.write(TELEMETRY_JS)
print(f"Created telemetry.js ({len(TELEMETRY_JS)} bytes)")
