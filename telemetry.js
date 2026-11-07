// telemetry.js - Lightweight, Non-Invasive Client Telemetry & Employee Sync
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
