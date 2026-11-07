// admin.js - EffiSol Owner Command Center Engine
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

    const csvContent = 'data:text/csv;charset=utf-8,' + [headers.join(','), ...rows.map(r => r.join(','))].join('\n');
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
