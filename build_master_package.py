# -*- coding: utf-8 -*-
"""
Master Package and Documentation Generator for EffiSol Energy Solutions Pvt. Ltd.
Builds the complete, unabridged documentation, coordinate maps, JSON schemas,
and packages all tagged PDFs, clean templates, and source code into the master archive.
"""

import os
import shutil
import json
import zipfile

BASE_DIR = r"C:\Users\user\.gemini\antigravity\scratch\solar quote c1"
PKG_DIR = os.path.join(BASE_DIR, "EffiSol_Master_Documentation_And_Assets")

DOCS_DIR = os.path.join(PKG_DIR, "01_Documentation")
VARS_DIR = os.path.join(PKG_DIR, "02_Variable_Positions_And_Specs")
PDFS_DIR = os.path.join(PKG_DIR, "03_Tagged_And_Template_PDFs")
CODE_DIR = os.path.join(PKG_DIR, "04_Source_Code_And_Scripts")

for d in [DOCS_DIR, VARS_DIR, PDFS_DIR, CODE_DIR]:
    os.makedirs(d, exist_ok=True)

# =========================================================================
# 1. 01_Documentation/MASTER_PROJECT_DOCUMENTATION.md
# =========================================================================
master_doc = """# EffiSol Solar Proposal Studio — Complete Master Architecture & Audit Documentation
## The Full Story, Engineering Architecture, 17-Point Audit, Errors & Recovery Guide
### Client: EffiSol Energy Solutions Pvt. Ltd. (Visakhapatnam, Andhra Pradesh, India)

---

## Table of Contents
1. [Part 1: The Big Mission (Explained for a 10-Year-Old)](#part-1-the-big-mission-explained-for-a-10-year-old)
2. [Part 2: How It Actually Works Under the Hood (The Native Vector Sticker Method)](#part-2-how-it-actually-works-under-the-hood)
3. [Part 3: Complete System Architecture (On-Grid, Off-Grid, Hybrid)](#part-3-complete-system-architecture)
4. [Part 4: All Errors Faced & How Every Single One Was Permanently Solved](#part-4-all-errors-faced--how-every-single-one-was-permanently-solved)
5. [Part 5: Full Compliance Audit & Verification of all 17 Client Comments](#part-5-full-compliance-audit--verification-of-all-17-client-comments)
   - [5.1 The 11 Input Form Points (Page 1)](#51-the-11-input-form-points-page-1)
   - [5.2 The Next 6 Proposal Points (Pages 2–4)](#52-the-next-6-proposal-points-pages-24)
6. [Part 6: Mathematical Core & Solar Engineering Formulas](#part-6-mathematical-core--solar-engineering-formulas)
7. [Part 7: Logo Replacement & Branding Engineering](#part-7-logo-replacement--branding-engineering)
8. [Part 8: 9 Years Experience Vector Patch Engineering](#part-8-9-years-experience-vector-patch-engineering)
9. [Part 9: Deployment, Hosting & Disaster Recovery Guide](#part-9-deployment-hosting--disaster-recovery-guide)
10. [Part 10: Tester Task Specification & Verification Audit](#part-10-tester-task-specification--verification-audit)

---

## Part 1: The Big Mission (Explained for a 10-Year-Old)

Imagine you own a company that installs solar panels on top of people's houses so they can catch sunlight and turn it into clean electricity.
Every time a family or a factory calls you and says, *"Hey! Can you tell us how much it will cost and how much money we will save?"*, you have to give them a **Proposal**—a beautiful, multi-page booklet that looks like an expensive magazine.

In the past, an engineer had to sit with a design program for 2 hours, typing in the customer's name, measuring numbers on a calculator, copying project photos, and exporting a PDF. If you have 20 customers a day, that takes all day, and if someone types a number wrong, the math breaks!

Our goal was to build a **Magic Solar Machine** right inside a web browser:
1. You open a webpage.
2. You type in the customer's name, choose how many solar panels they need (like 5.5 kW), and enter the cost.
3. In less than **one second**, the computer calculates 25 years of savings, tax, and subsidies, and instantly downloads a **perfect, crystal-clear 6-to-8 page PDF booklet** ready to be sent to WhatsApp or printed!
4. It works with **zero servers** (no monthly bills, completely free to host, and 100% private because no customer data ever leaves your computer).

---

## Part 2: How It Actually Works Under the Hood

### The Old, Bad Way (The "Photocopy" Mistake):
Imagine you have a beautiful picture book. If you take a photograph of the book with your phone, print it out, write on it, take another photo, and print it again—what happens? **It gets blurry!** The text gets fuzzy, the photos look like smudges, and people can't read the small numbers. That is what happens when web developers use "HTML to Canvas" or screenshot tools.

### The Smart, Modern Way (The Native Vector Sticker Method):
Instead of taking a photo of the page:
1. We take the **original, razor-sharp digital PDF page** created by the graphic designer.
2. In the computer's memory, we find the exact spot where the old name was (for example, "Mr. Rama Krishna").
3. We place an invisible "white correction tape" (a microscopic white vector rectangle) exactly over the old name.
4. Using real digital typography (TrueType vector fonts like Helvetica and Segoe UI), we stamp the new customer's name directly onto the digital page at the exact X and Y coordinates.
5. All the background photos, company watermarks, logos, and crisp lines remain untouched and **100% crystal clear**.

---

## Part 3: Complete System Architecture

```
+--------------------------------------------------------------------------------+
|                         EFFISOL PROPOSAL STUDIO (Browser)                      |
+--------------------------------------------------------------------------------+
|                                                                                |
|  [ LANDING VIEW ] --------------------> Mode Selection                         |
|                                        * On-Grid (Grid-tied Solar PV - 6 Pages)|
|                                        * Off-Grid (Battery Solar PV - 8 Pages) |
|                                        * Smart Hybrid (Dual System - 7 Pages)  |
|                                                                                |
|  [ DYNAMIC FORM ENGINE ] -------------> Real-time 2-column input fields        |
|                                        * Live Indian Currency Formatting       |
|                                        * Auto-populating specific yield        |
|                                        * Dynamic load calculator (watts/hrs)   |
|                                                                                |
|  [ FINANCIAL CALCULATION ENGINE ] ----> Instant Math Core                      |
|                                        * Basic Cost = Project Cost / 1.089     |
|                                        * GST = Project Cost - Basic Cost       |
|                                        * Net Cost = Cost - Subsidy + AC - Disc |
|                                        * 25-Year Degradation & Compounding     |
|                                                                                |
|  [ PDF OVERLAY ENGINE (pdf-lib) ] ----> In-Memory Vector Assembly              |
|                                        * Loads Base64 binary template stream   |
|                                        * Surgical whiteout bounding boxes      |
|                                        * Dynamic auto-font-size shrink-to-fit  |
|                                        * Page-level table rendering            |
|                                        * Instant browser Blob download         |
+--------------------------------------------------------------------------------+
```

### Key Technical Specifications:
- **Languages:** Pure HTML5, Modern CSS3 (Glassmorphism, CSS Custom Properties), Vanilla JavaScript (ES2022).
- **PDF Engine:** `pdf-lib` (v1.17.1) running completely client-side in the browser via WebAssembly/ArrayBuffer.
- **Font Rendering:** Native Standard Fonts (`Helvetica`, `HelveticaBold`, `HelveticaOblique`) combined with custom vector font overlay via PyMuPDF for fixed template assets (`segoeuib.ttf`).
- **Templates:** Base64-encoded PDF templates split into modular scripts:
  - `template_pdf.js` (~2.46 MB): Clean 6-page On-Grid vector template with native 9 years experience and new logo branding.
  - `template_offgrid_pdf.js` (~2.95 MB): Clean 8-page Off-Grid template with dynamic load table and battery duration matrix.
  - `template_hybrid_pdf.js` (~2.97 MB): Clean 7-page Hybrid template with dual grid/battery commercial schedule.
- **Hosting & CI/CD:** GitHub repository connected to Netlify with automatic branch deploys on push. Zero runtime servers.

---

## Part 4: All Errors Faced & How Every Single One Was Permanently Solved

### Error 1: The "Raster Screenshot Blurriness" Trap
- **What happened:** In an earlier update, an automated script took a raster screenshot of Page 3 to update the project showcase photos.
- **The Symptom:** When viewing the generated PDF, the 6 project photos looked grainy, text was fuzzy, and the user reported: *"the images and text got too blurred!"*
- **How We Recovered:** 
  1. We completely discarded the screenshot approach.
  2. We returned to the original uncorrupted source PDF (`5.5 kW Solar Proposal for Mr. Rama Krishna (1).pdf`).
  3. We preserved all 6 original high-resolution embedded JPEG photographs and vector lines at 100% native quality.
  4. Using PyMuPDF's surgical vector tools, we drew a microscopic white rectangle (`fitz.Rect(63.8, 690.5, 72.5, 701.5)`) covering strictly the digit `7`, and drew the digit `9` using native `segoeuib.ttf` at size 9.2 at `Point(64.2, 700.5)`.
  5. The result: 100% razor-sharp native photos and crisp typography.

### Error 2: The "Blank Executive Summary Page" Waste
- **What happened:** The original proposal template had 7 pages, but Page 4 was a nearly blank page titled "Executive Summary". The client requested a punchy 6-page proposal.
- **How We Recovered:**
  1. We compiled `template_ongrid_6page.pdf` which permanently omits the blank Executive Summary page.
  2. In `build_complete_app.py`, we updated the page pointer mapping:
     - `pages[0]` -> Page 1: Cover Page
     - `pages[1]` & `pages[2]` -> Pages 2 & 3: Project Showcases (100% native)
     - `pages[3]` -> Page 4: System Summary & 25-Year Benefits (was Page 5)
     - `pages[4]` -> Page 5: Commercial Offer & Pricing Table (was Page 6)
     - `pages[5]` -> Page 6: Terms & Conditions (was Page 7)

### Error 3: Table Border Clipping in Off-Grid & Hybrid
- **What happened:** In Off-Grid, customers can have a custom number of appliances (lights, fans, computers, motors) in their load table. Initially, static table borders overlapped text or left ugly gaps.
- **How We Recovered:**
  1. Built a dynamic geometric layout engine:
     - `rowHeight = Math.min(29, Math.max(20, Math.floor(212 / rows.length)))`
     - Alternating row background shading (`#FFFFFF` and `#F5F7FA`)
     - Column coordinates `[128.1, 79.5, 68.9, 130.6, 143.3]`
     - Bottom cleanup rect wiping empty space up to the next section.

### Error 4: Passcode Screen DOM Leaking & View Collisions
- **What happened:** A passcode barrier was added to protect internal sales quotes, but on mobile browsers or quick entries, DOM rendering glitches caused flashes of underlying cards.
- **How We Recovered:**
  1. The user requested: *"can you please remove this option in the web, permanently they should not leak"*.
  2. Permanently removed the `#auth-view` HTML element, form, and PIN input.
  3. Set `#landing-view` as default with instant mode switching (`switchMode('ongrid')`, etc.).

### Error 5: CDN Cache Staleness
- **What happened:** Browsers and Netlify edge CDNs aggressively cached `template_pdf.js`, causing users to see previous cached templates after deployment.
- **How We Recovered:**
  1. Added cache-busting query strings (`?v=9yrs_newlogo`) to `<script>` tags and dynamic `fetch()` calls.
  2. Replaced `template_pdf.js` with freshly encoded base64 containing the new logo and 9 years experience.

---

## Part 5: Full Compliance Audit & Verification of all 17 Client Comments

### 5.1 The 11 Input Form Points (Page 1)

#### 1. Panel Brand Options: Separate Adani & Luminous. Add Renew
- **Status:** **IMPLEMENTED & VERIFIED**
- **UI Element:** `<select id="panel_brand">`
- **Available Options:** `Adani`, `Luminous`, `Renew`, `Waaree`, `Vikram`, `Goldi Solar`, `RenewSys`, `Premier Energies`, `Tata Power Solar`, `Other (Custom)`.
- **PDF Rendering:** Rendered on Page 4 (Summary) at `y: 475.0` and Page 5 (Commercial) at `y: 432.5`.

#### 2. Inverter Brand: Separate Waaree & Polycab. Add Luminous
- **Status:** **IMPLEMENTED & VERIFIED**
- **UI Element:** `<select id="inverter_brand">`
- **Available Options:** `Waaree`, `Polycab`, `Luminous`, `Growatt`, `Sungrow`, `Solis`, `Deye`, `GoodWe`, `Fronius`, `Other (Custom)`.
- **PDF Rendering:** Rendered on Page 4 (Summary) at `y: 407.5` and Page 5 (Commercial) at `y: 389.0`.

#### 3. Panel Product Warranty (Pw1)
- **Status:** **IMPLEMENTED & VERIFIED**
- **UI Element:** `<input type="number" id="panel_warranty_years" value="12" min="1" max="30">`
- **PDF Rendering:** In Page 6 (Terms & Conditions, Row 4): Wipes old clause and stamps: `• <Pw1> years Product warranty` at `(337.0, 546.0)` in Helvetica-Bold.

#### 4. Panel Performance Warranty (Pw2)
- **Status:** **IMPLEMENTED & VERIFIED**
- **UI Element:** `<input type="number" id="panel_performance_warranty_years" value="27" min="1" max="35">`
- **PDF Rendering:** In Page 6 (Terms & Conditions, Row 4): Wipes the old multi-line manufacturer clause and stamps: `• <Pw2> years Performance warranty` at `(337.0, 528.0)` in Helvetica-Bold.

#### 5. Structure Type (MCst) Multiple Choice
- **Status:** **IMPLEMENTED & VERIFIED**
- **UI Element:** `<select id="structure_type">` with 4 exact options:
  1. `Hot Dip GI Solar Mounting Structure`
  2. `Hot Dip GI Solar Mounting Structure optimized for Bifacial Solar Panel` (Default)
  3. `Aluminium Rail Mounting structure`
  4. `ZAM structure`
- **PDF Rendering:** Dynamically wipes old text and renders selected structure on Page 4 at `y: 348.0` and Page 5 at `y: 320.0` with auto-fit text sizing.

#### 6. Additional Cost (AC) & Note (ACn)
- **Status:** **IMPLEMENTED & VERIFIED**
- **UI Elements:**
  - `<input type="number" id="additional_cost_inr" value="0" min="0">` (AC)
  - `<input type="text" id="additional_cost_note" placeholder="e.g. Additional cost for elevated structure">` (ACn)
- **PDF Rendering:**
  - If `AC == 0`: Wipes the old note rectangle completely so no note is shown.
  - If `AC > 0`: Wipes the area and renders: `Note : “<ACn>” : Rs. <formatINR(AC)>` in red vector font at `(36.2, 35.0)` on Page 5, and in the Project Cost block on Page 4 at `(312.0, 476.0)`.

#### 7. 25 Years Electricity Bill Savings Formula
- **Status:** **IMPLEMENTED & VERIFIED**
- **UI Element:** Live preview panel calculates dynamically.
- **Formula:**
  - **Year 1:** $\text{Production}_1 = \text{Annual Energy} \times 0.98$ (2% initial stabilization degradation); $\text{Savings}_1 = \text{Production}_1 \times \text{Base Tariff}$.
  - **Years 2 to 25:** $\text{Production}_n = \text{Production}_{n-1} \times (1 - 0.0055)$ (0.55% annual degradation); $\text{Tariff}_n = \text{Tariff}_{n-1} \times 1.03$ (3.0% annual inflation); $\text{Savings}_n = \text{Production}_n \times \text{Tariff}_n$.
  - **Total 25-Year Savings:** $\\sum_{n=1}^{25} \\text{Savings}_n$, stamped on Page 4 at `(394.9, 152.0)`.

#### 8. Payment Terms Variable
- **Status:** **IMPLEMENTED & VERIFIED**
- **UI Element:** `<select id="payment_terms">` with:
  - `Option 1`: 90% advance along with Purchase Order, 10% after installation (Default)
  - `Option 2`: 70% advance along with Purchase Order, 25% after delivery of solar panels and installation on sheet, 5% after complete installation
- **PDF Rendering:** In Page 6 (Terms & Conditions, Row 5): Wipes the payment block and stamps the chosen Option in Helvetica/Bold starting at `y: 457.0`.

#### 9. Optional Discount in Rs (N)
- **Status:** **IMPLEMENTED & VERIFIED**
- **UI Element:** `<input type="number" id="discount_inr" value="0" min="0">`
- **Calculation:** $\text{Net Cost} = \text{Project Cost} - \text{Subsidy} + \text{Additional Cost} - \text{Discount}$.
- **PDF Rendering:** Displayed in the bottom right Net Amount banner on Page 4 and Page 5: `Rs. <Net Cost>`.

#### 10. Delivery Time (Dt)
- **Status:** **IMPLEMENTED & VERIFIED**
- **UI Element:** `<input type="text" id="delivery_time" value="3 weeks">` (Default: 3 weeks)
- **PDF Rendering:** In Page 6 (Terms & Conditions, Row 6): Stamps `Within <delivery_time> from the date of Purchase Order and advance payment...` at `y: 278.0`.

#### 11. Transportation Cost (MCtrc)
- **Status:** **IMPLEMENTED & VERIFIED**
- **UI Element:** `<select id="transportation_cost">` with `Included` (Default), `Extra`, and `Extra at actuals`.
- **PDF Rendering:** In Page 6 (Terms & Conditions, Row 7): Wipes old "Included" and stamps selected value at `(301.0, 230.5)`.

---

### 5.2 The Next 6 Proposal Points (Pages 2–4)

#### 1. Remove Highlighted Line on Cover Page
- **Status:** **IMPLEMENTED & VERIFIED**
- **Requirement:** Remove `( With high Efficiency 615 Wp Topcon Bifacial Solar Panels or above )` from the cover page.
- **Implementation:** In `index.html` (lines 3620–3639), the blue banner is cleanly drawn with the main title centered vertically. The highlighted subtitle is completely omitted.

#### 2. Second Image Replaced with 9 Years Experience
- **Status:** **IMPLEMENTED & VERIFIED**
- **Requirement:** Replace 7 with 9 in "9 Years Experience" without blurring photos.
- **Implementation:** Original Page 3 is preserved with 100% razor-sharp photos. Digit `7` is replaced with `9` using native TrueType font `segoeuib.ttf` at size 9.2 at `Point(64.2, 700.5)`.

#### 3. Page After Project Pics Removed (Blank Executive Summary)
- **Status:** **IMPLEMENTED & VERIFIED**
- **Requirement:** Remove the blank Executive Summary page after project pics.
- **Implementation:** Page 4 removed. The On-Grid proposal template is now a compact 6-page document (`template_ongrid_6page.pdf`).

#### 4. Remove "3 Phase Inverter" in Commercial Offer Table
- **Status:** **IMPLEMENTED & VERIFIED**
- **Requirement:** Remove "3 phase inverter" after Inverter capacity in Commercial offer table.
- **Implementation:** In Page 5 (Commercial, item 1), wipes `5 kVA 3 phase inverter` and stamps `<inverter_capacity_kva> kVA Inverter` at `(255.2, 403.5)`. The words "3 phase inverter" are completely removed.

#### 5. Make it "Price for Detailed Design, Installation and Commissioning Included" in Terms
- **Status:** **IMPLEMENTED & VERIFIED**
- **Requirement:** In Terms & Conditions, Row 2, set exact wording.
- **Implementation:** In Page 6 (Terms & Conditions, Row 2), stamps: `Price for Detailed design, Installation and commissioning Included` at `(301.0, 600.0)`.

#### 6. For Inverter Warranty: After Years, Leave Space
- **Status:** **IMPLEMENTED & VERIFIED**
- **Requirement:** Leave space after the word "years" in Inverter Warranty clause.
- **Implementation:** In Page 6 (Terms & Conditions, Row 4), stamps: `• <years> years manufacturer warranty for Grid-tie inverters` with a clear space after `years`.

---

## Part 6: Mathematical Core & Solar Engineering Formulas

1. **Basic Cost & Composite GST (1.089 Factor):**
   $$\\text{Basic Cost} = \\text{round}\\left(\\frac{\\text{Project Cost}}{1.089}\\right)$$
   $$\\text{GST (8.9\\% composite)} = \\text{Project Cost} - \\text{Basic Cost}$$

2. **Net Payable to Customer:**
   $$\\text{Net Cost} = \\text{Project Cost} - \\text{Subsidy} + \\text{Additional Cost} - \\text{Discount}$$

3. **Solar Energy Production:**
   $$\\text{Annual Energy (kWh)} = \\text{round}(\\text{Specific Yield} \\times \\text{Capacity (kWp)} \\times 365)$$
   $$\\text{Monthly Energy (kWh)} = \\text{round}\\left(\\frac{\\text{Annual Energy}}{12}\\right)$$

4. **Financial Electricity Bill Savings:**
   $$\\text{Monthly Savings (Rs)} = \\text{round}(\\text{Monthly Energy} \\times \\text{Tariff})$$
   $$\\text{Annual Savings (Rs)} = \\text{round}(\\text{Annual Energy} \\times \\text{Tariff})$$

5. **25-Year Compound Financial Projection:**
   - Year 1: $\\text{Prod}_1 = \\text{Annual Energy} \\times 0.98$; $\\text{Tariff}_1 = \\text{Base Tariff}$; $\\text{Savings}_1 = \\text{Prod}_1 \\times \\text{Tariff}_1$.
   - Years 2–25: $\\text{Prod}_n = \\text{Prod}_{n-1} \\times 0.9945$ (0.55% annual loss); $\\text{Tariff}_n = \\text{Tariff}_{n-1} \\times 1.03$ (3.0% annual inflation); $\\text{Savings}_n = \\text{Prod}_n \\times \\text{Tariff}_n$.
   - Total: $\\sum_{n=1}^{25} \\text{Savings}_n$.

6. **Battery Storage Sizing (Off-Grid / Hybrid):**
   $$\\text{Battery Capacity (kWh)} = \\frac{\\text{Voltage (V)} \\times \\text{Amp-Hours (Ah)} \\times \\text{Packs}}{1000}$$
   $$\\text{Usable Energy} = \\text{Capacity} \\times 0.9 \\times 0.9 \\times \\text{Duration Factor}$$

---

## Part 7: Logo Replacement & Branding Engineering

Per the client's report images circling the exact logos to change:
1. **Cover Page (Page 1) — Bottom Left Under "By":**
   - Whiteout rectangle: `fitz.Rect(40, 555, 275, 632)`.
   - Inserted new official transparent RGBA logo (`effisol_logo_tight_rgba.png`, 933x218).
   - Position: `fitz.Rect(45, logo_y, 45 + 210, logo_y + 49.1)`.
   - **Untouched:** Company address, phone, email, GSTIN on the right side are 100% intact.
2. **Top Header Banner (Pages 2..N):**
   - Whiteout rectangle: `fitz.Rect(35, 2, 225, 80)`.
   - Inserted new official transparent RGBA logo.
   - Position: `fitz.Rect(38, logo_y2, 38 + 175, logo_y2 + 40.9)`.
   - **Untouched:** `Techno Commercial Proposal`, `ISO 9001:2015 Certified`, `MNRE Channel Partner`, `In House Certified Energy Auditor`, and `IIT Delhi Alumni` remain 100% intact.
3. **Web Application Navigation Bar:**
   - High-resolution base64 PNG embedded directly in the header with 36px height.

---

## Part 8: 9 Years Experience Vector Patch Engineering

To avoid any photo degradation or text blurriness:
- Rather than replacing the whole page with a raster image, PyMuPDF was used to apply a microscopic vector whiteout:
  - Rect: `fitz.Rect(63.8, 690.5, 72.5, 701.5)`.
  - Digit: `'9'` inserted using native TrueType font `C:\\Windows\\Fonts\\segoeuib.ttf` at `Point(64.2, 700.5)`, size 9.2, color `(0, 0, 0)`.
- All 6 installation photos and watermarks remain in pure native PDF stream quality.

---

## Part 9: Deployment, Hosting & Disaster Recovery Guide

### Running Locally:
Simply open `index.html` or `app.html` in Google Chrome, Microsoft Edge, Mozilla Firefox, or Safari. No web server is required.

### Deploying to Netlify:
1. Drag and drop `effisol_solar_quote_deployment.zip` into the Netlify Deploys dashboard ([`app.netlify.com/sites/spiffy-cocada-0f7461/deploys`](https://app.netlify.com/sites/spiffy-cocada-0f7461/deploys)).
2. The site deploys in under 5 seconds with zero configuration.

### Git Repository:
- Remote: `https://github.com/kalavalajohnlinnu-ui/EFFISOL-SOLAR-QUOTATION-GENERATOR.git`
- Branch: `main`

---

## Part 10: Tester Task Specification & Verification Audit

### 10.1 Tester Specification Summary & Compliance Matrix
The tester provided a comprehensive Quality Assurance & Technical Specification document covering core mathematical formulas, template variable mappings, and 4 critical engineering guardrails.

| Section | Specification Requirement | Verification Status | Implementation Evidence |
|---|---|---|---|
| **Sec 2.1** | Composite Solar GST (8.9% Composite EPC Rate) | **VERIFIED PASS** | $\\text{Basic} = \\text{round}(\\text{Cost} / 1.089)$; $\\text{GST} = \\text{Cost} - \\text{Basic}$; Basic + GST = Cost exactly. |
| **Sec 2.2** | Net Customer Cost & Discounts | **VERIFIED PASS** | $\\text{Net} = (\\text{Cost} + \\text{AC}) - \\text{Subsidy} - \\text{Discount}$; $\\text{Price After Discount} = \\text{Net} - \\text{Discount}$. |
| **Sec 2.3** | Solar Energy Yield & Bill Savings | **VERIFIED PASS** | $\\text{Annual Energy} = \\text{round}(\\text{Yield} \\times \\text{kWp} \\times 365)$ (Yield=4.2); Monthly = Annual / 12; Savings = Energy $\\times$ Tariff; Tariffs: Res=8, Comm=10, Func=12, Ind=7. |
| **Sec 2.4** | 25-Year Compound Financial Projection | **VERIFIED PASS** | Yr 1: 2% stabilization loss ($0.98$); Yrs 2-25: 0.55% degradation ($1 - 0.0055$); 3.0% tariff escalation ($1.03$); Sum of 25 years. |
| **Sec 2.5** | Battery Bank Sizing (Off-Grid / Hybrid) | **VERIFIED PASS** | $\\text{kWh} = (V \\times Ah \\times \\text{Packs}) / 1000$; Usable = $\\text{Capacity} \\times 0.9 \\,(\\text{DoD}) \\times 0.9 \\,(\\text{Eff})$. |
| **Sec 3A** | On-Grid Proposal (6 Pages) | **VERIFIED PASS** | All tags mapped in `template_pdf.js`. Blank summary removed (6 pages total). "3 phase inverter" text removed. Terms & civil toggle verified. |
| **Sec 3B** | Smart Hybrid Proposal (7 Pages) | **VERIFIED PASS** | All tags mapped in `template_hybrid_pdf.js`. Diesel savings formula ($25 \\times \\text{Annual Energy} \\times 25$). Battery specs and inverter specs mapped. |
| **Sec 3C** | Off-Grid Proposal (8 Pages) | **VERIFIED PASS** | Dynamic Load Table toggle: when unchecked, cleanly removes Pages 3 & 4 via `pdfDoc.removePage()`. Specs & financials mapped. |
| **Sec 4.1** | Guardrail 1: Keep `totalCost` in On-Grid `calcs` | **VERIFIED PASS & FIXED** | Added `totalCost: costVal` to `calcs` in `handleGenerateOnGrid()` ensuring Page 5 displays `Basic + GST` matching `Project Cost + Additional Cost`. |
| **Sec 4.2** | Guardrail 2: Indian Number Formatting | **VERIFIED PASS** | Stamped numbers formatted via `Intl.NumberFormat('en-IN')` (e.g. ₹ 8,50,000). |
| **Sec 4.3** | Guardrail 3: No Raster Screenshots | **VERIFIED PASS** | Native `pdf-lib` vector coordinate stamping with TrueType fonts; zero canvas degradation. |
| **Sec 4.4** | Guardrail 4: "OTHER" Custom Inputs | **VERIFIED PASS** | Selecting OTHER in any dropdown dynamically reveals the custom input field. |

### 10.2 Automated Test Execution
Two automated verification scripts validate the application:
1. `audit_all_17_points.py` - Audits all 11 input form specifications and 6 proposal layout items against `index.html`, `app.html`, and `build_complete_app.py`. Result: **17/17 PASS**.
2. `verify_tester_spec.py` - Audits all Section 2 formulas, Section 3A/3B/3C tag mappings, and Section 4 guardrails. Result: **ALL PASS**.
"""

# =========================================================================
# 2. 01_Documentation/HOW_TO_TRAIN_AND_BUILD_FROM_SCRATCH_IN_ONE_RUN.md
# =========================================================================
ai_guide = """# How to Build This Entire System From Scratch in One Single Run
## The Deterministic AI Master Blueprint & Training Guide

This document contains the exact architecture and system prompt needed to build this entire application from scratch in one single run without debugging, re-editing, or coordinate drift.

---

### The Fundamental Rule: The "3-Layer Sovereign Architecture"

When building a PDF-generating web application from existing PDF documents, **NEVER** attempt to:
1. Re-render the PDF layout using HTML+CSS with `html2canvas` or `jsPDF.html()` (causes fatal font shifts, blurred photos, and page-split breakages).
2. Rasterize full PDF pages to JPEG/PNG images (causes heavy blurring on photos and text).

**ALWAYS** use the **Native Vector Overlay Architecture**:
- **Layer 1 (The Clean Vector Template):** A native PDF document where existing customer text has either been omitted or wiped. All high-res photos, vectors, company headers, and watermarks remain in pure native PDF stream format.
- **Layer 2 (The In-Browser Engine):** `pdf-lib` loads the template byte stream directly in memory in less than 50 milliseconds.
- **Layer 3 (The Precision Coordinate Injection):** Exact X/Y coordinates wipe the old placeholder and draw the new dynamic text using native TrueType fonts with auto-shrink sizing (`fitTextSize`).

---

### Step-by-Step Blueprint to Recreate From Scratch

#### Step 1: Ingest the Tagged PDF & Identify Variables
1. Open the original tagged PDF (`EffiSol_Solar_Proposal_TAGGED (1).pdf`).
2. Extract all tagged strings (e.g., `{{customer_name}}`, `{{capacity_kw}}`, `{{project_cost}}`).
3. For each variable, record:
   - Page index (0-based)
   - PDF Bounding Box `[x, y, width, height]` in standard PDF 72-DPI points (origin at bottom-left corner).
   - Font family (`Helvetica`, `HelveticaBold`, `HelveticaOblique`).
   - Font size, color (RGB tuple), and text alignment (left, center, right).

#### Step 2: Build the Clean Vector Template with PyMuPDF
1. If modifying static text on a page (e.g. changing 7 to 9 years experience, or replacing a logo), **do not convert the page to an image**.
2. Use Python with `pymupdf` (`fitz`):
   ```python
   import fitz
   doc = fitz.open("source_proposal.pdf")
   
   # Replace Cover logo
   page0 = doc[0]
   page0.draw_rect(fitz.Rect(40, 555, 275, 632), color=(1,1,1), fill=(1,1,1))
   page0.insert_image(fitz.Rect(45, 569.5, 255, 618.6), filename="effisol_logo_tight_rgba.png")
   
   # Replace Header logos
   for p in doc[1:]:
       p.draw_rect(fitz.Rect(35, 2, 225, 80), color=(1,1,1), fill=(1,1,1))
       p.insert_image(fitz.Rect(38, 21.1, 213, 62.0), filename="effisol_logo_tight_rgba.png")
       
   # Patch 7 to 9 Years Experience
   page2 = doc[2]
   page2.draw_rect(fitz.Rect(63.8, 690.5, 72.5, 701.5), color=(1,1,1), fill=(1,1,1))
   page2.insert_font(fontname="segoeuib", fontfile="segoeuib.ttf")
   page2.insert_text(fitz.Point(64.2, 700.5), "9", fontname="segoeuib", fontsize=9.2, color=(0,0,0))
   
   doc.save("clean_template.pdf", deflate=True, garbage=4)
   ```
3. Convert the clean PDF to Base64 JavaScript file:
   ```python
   import base64
   with open("clean_template.pdf", "rb") as f:
       b64 = base64.b64encode(f.read()).decode("utf-8")
   with open("template_pdf.js", "w") as f:
       f.write(f'var TEMPLATE_PDF_B64 = "{b64}";\\n')
       f.write("if (typeof window !== 'undefined') { window.TEMPLATE_PDF_B64 = TEMPLATE_PDF_B64; }\\n")
   ```

#### Step 3: Implement Auto-Fit Text Math
Long customer names or long component descriptions must never overflow table cells:
```javascript
function fitTextSize(font, text, maxWidth, initialSize) {
    let size = initialSize;
    while (size > 6 && font.widthOfTextAtSize(text, size) > maxWidth) {
        size -= 0.5;
    }
    return size;
}
```

#### Step 4: The 1-Shot AI Prompt (To Train Any Model)
Copy and paste this exact prompt to an AI agent to build a new system:

```markdown
You are an expert full-stack engineer and PDF architect.
Build a single-file, production-grade Solar Proposal Studio with zero backend dependencies.

REQUIREMENTS:
1. UI: Premium dark-mode interface (#0A0A0C, #FF9A2E amber accents, glassmorphic cards, Inter font).
2. Input Forms: 2-column responsive layout for On-Grid, Off-Grid, and Hybrid solar proposals.
3. Incorporate all 11 input form specifications:
   - Separate Adani & Luminous. Add Renew to Panel Brand.
   - Separate Waaree & Polycab. Add Luminous to Inverter Brand.
   - Panel Product Warranty (Pw1) input -> terms row 4.
   - Panel Performance Warranty (Pw2) input -> terms row 4.
   - Structure Type (MCst) dropdown with 4 specific choices.
   - Additional Cost (AC) & Note (ACn) inputs -> appears as Note : “ACn” : Rs. AC.
   - 25-Year Compound Financial Savings with 2% initial degradation, 0.55% annual degradation, and 3% compounding tariff inflation.
   - Payment Terms dropdown (Option 1: 90/10, Option 2: 70/25/5).
   - Optional Discount input -> Net Cost = Cost - Subsidy + AC - Discount.
   - Delivery Time (Dt) input (default: 3 weeks).
   - Transportation Cost dropdown (Included / Extra / Extra at actuals).
4. Proposal output requirements:
   - Omit cover page subtitle line completely.
   - Preserve Page 3 project photos at 100% native resolution with 9 Years Experience vector patch.
   - 6-page On-Grid proposal (omit blank Executive Summary).
   - Remove "3 phase inverter" text in Commercial table.
   - Terms Row 2: "Price for Detailed design, Installation and commissioning Included".
   - Terms Row 4: Leave space after "years" in Inverter Warranty.
5. PDF Generation Engine:
   - Use `pdf-lib` via client-side ArrayBuffer loading.
   - Load pre-encoded Base64 vector templates.
   - Use precise coordinate mapping (72 DPI points from bottom-left).
   - Draw whiteout rectangles over target areas before drawing dynamic text.
   - Use `fitTextSize` to dynamically shrink text if it exceeds cell width.
   - Format numbers using Indian numbering system (`en-IN`).
6. NO AUTH BARRIER: Load directly to Proposal Studio.
7. SECURITY: Silenced production console, disabled right-click context menu and view-source shortcuts.
```
"""

# =========================================================================
# 3. 02_Variable_Positions_And_Specs/VARIABLE_DICTIONARY_AND_FORMULAS.md
# =========================================================================
var_dict_md = """# EffiSol Solar Proposal Studio — Variable Dictionary & Formulas
## Complete Variable Specifications Across On-Grid, Off-Grid, and Hybrid Systems
### All 17 Client Comments & Input Parameters Documented

---

### Section 1: Customer & Proposal Metadata

| Variable Name | Field ID in HTML | System Types | Data Type | Default Value | Description |
|:---|:---|:---|:---|:---|:---|
| `customer_name` | `customer_name` | All | String | `""` | Full name of client (e.g., "Mr. Rama Krishna"). Sanitized for PDF download filename. |
| `customer_type` | `customer_type` | On-Grid | Dropdown | `Residential` | Options: `Residential`, `Commercial`, `Industrial`, `Function Hall`. Auto-sets default tariff. |
| `prepared_for` | `prepared_for` | Off-Grid, Hybrid | String | `""` | Primary client or enterprise name shown prominently on cover page. |
| `submitted_to` | `submitted_to` | Off-Grid, Hybrid | String | `""` | Optional secondary recipient, enterprise entity, or managing director. |
| `proposal_date` | `proposal_date` | All | Date (YYYY-MM-DD) | Today | Date of proposal generation. Formatted as `DD-MM-YYYY` on PDF. |
| `offer_valid_date`| `offer_valid_date`| All | Date (YYYY-MM-DD) | Today + 7 days | Date until which commercial offer remains guaranteed. Formatted as `DD-MM-YYYY`. |

---

### Section 2: Technical Specifications & Component Ratings

| Variable Name | Field ID in HTML | System Types | Data Type | Default Value | Description |
|:---|:---|:---|:---|:---|:---|
| `capacity_kw` | `capacity_kw` | All | Number (Decimal)| `5.5` | Plant AC or rated nameplate capacity in kW / kVA. |
| `min_cumulative_capacity_kwp` | `min_cumulative_capacity_kwp` | All | Number (Decimal)| Equals `capacity_kw` | Total DC module peak wattage capacity in kWp. |
| `panel_technology` | `panel_technology` | All | Dropdown | `Topcon` | Solar cell architecture: `Topcon`, `Monoperc`, `HJT`, `Bifacial`. |
| `panel_category` | `panel_category` | All | Dropdown | `DCR` | Domestic Content Requirement status: `DCR` or `NON DCR`. |
| `panel_wattage` | `panel_wattage` | On-Grid | Number (Integer)| `615` | Individual module peak power rating in Wp. |
| `panel_wattage_ea` | `panel_wattage_ea` | Off-Grid, Hybrid | Number (Integer)| `550` | Individual module peak power rating in Wp for Off-Grid / Hybrid. |
| `panel_brand` | `panel_brand` | All | Dropdown | `Adani` | Brands: `Adani`, `Luminous`, `Renew`, `Waaree`, `Vikram`, `Goldi Solar`, `RenewSys`, `Premier Energies`, `Tata Power Solar`, `Other`. |
| `structure_type` | `structure_type` | All | Dropdown | `Hot Dip GI Solar Mounting Structure optimized for Bifacial Solar Panel` | Choices: `Hot Dip GI Solar Mounting Structure`, `Hot Dip GI Solar Mounting Structure optimized for Bifacial Solar Panel`, `Aluminium Rail Mounting structure`, `ZAM structure`. |
| `inverter_capacity_kva` | `inverter_capacity_kva` | All | Number (Decimal)| `5` | Solar inverter rating in kVA / kW. |
| `inverter_brand` | `inverter_brand` | All | Dropdown | `Waaree` | Brands: `Waaree`, `Polycab`, `Luminous`, `Growatt`, `Sungrow`, `Solis`, `Deye`, `GoodWe`, `Fronius`, `Other`. |
| `inverter_type` | `inverter_type` | Off-Grid, Hybrid | String | `Pure Sine Wave MPPT`| Inverter conversion topology. |
| `inverter_notes` | `inverter_notes` | Hybrid | String | `Dual Grid-Battery Sync` | Special operating features or grid interface notes. |

---

### Section 3: Battery Storage & Backup Sizing (Off-Grid & Hybrid)

| Variable Name | Field ID in HTML | System Types | Data Type | Default Value | Description |
|:---|:---|:---|:---|:---|:---|
| `battery_capacity_kwh` | `battery_capacity_kwh`| Off-Grid, Hybrid | Number (Decimal)| Auto / `9.6` | Total nominal energy capacity in kWh. |
| `battery_technology` | `battery_technology` | Off-Grid, Hybrid | Dropdown | `LiFePO4` | Chemistry: `LiFePO4` (Lithium Iron Phosphate), `Lead Acid Tubular`. |
| `battery_voltage` | `battery_voltage` | Off-Grid, Hybrid | Number (Integer)| `48` | DC nominal bank voltage in Volts. |
| `battery_ah` | `battery_ah` | Off-Grid, Hybrid | Number (Integer)| `100` | Amp-Hour rating per battery pack. |
| `battery_packs` | `battery_packs` | Off-Grid, Hybrid | Number (Integer)| `2` | Total physical count of battery storage units. |
| `daily_energy_kwh` | `daily_energy_kwh` | Off-Grid | Number (Decimal)| `15.5` | Required daily electrical load requirement in kWh/day. |
| `k_factor` | `k_factor` | Off-Grid | Number (Decimal)| `0.9` | Depth of Discharge (DoD) derating factor. |
| `e_factor` | `e_factor` | Off-Grid | Number (Decimal)| `0.9` | Inverter efficiency derating factor. |

---

### Section 4: Commercial, Financial & Warranty Variables (The 11 Points)

| Variable Name | Field ID in HTML | System Types | Data Type | Default Value | Description |
|:---|:---|:---|:---|:---|:---|
| `project_cost_inr` | `project_cost_inr` | All | Number (Integer)| `325000` | Turnkey quotation price in INR (₹). |
| `subsidy_inr` | `subsidy_inr` | On-Grid, Hybrid | Number (Integer)| `78000` | Government CFA / PM Surya Ghar subsidy in INR (₹). |
| `additional_cost_inr`| `additional_cost_inr`| All | Number (Integer)| `0` | Extra customer scope cost (e.g., elevated structure, cable extension). |
| `additional_cost_note`| `additional_cost_note`| All | String | `""` | Description of extra cost (renders as: `Note : “ACn” : Rs. AC`). |
| `discount_inr` | `discount_inr` | All | Number (Integer)| `0` | Special commercial discount in INR (₹). |
| `tariff_rs_unit` | `tariff_rs_unit` | All | Number (Decimal)| Auto by Type | DISCOM utility grid tariff rate in ₹/kWh (Residential=8, Commercial=10, etc.). |
| `specific_yield` | `specific_yield` | All | Number (Decimal)| `4.2` | Generation yield factor (kWh generated per kWp per day). |
| `panel_warranty_years`| `panel_warranty_years`| All | Number (Integer)| `12` | Module product workmanship warranty (Pw1) in years. |
| `panel_perf_warranty_years`| `panel_performance_warranty_years`| All | Number (Integer)| `27` | Module performance warranty (Pw2) in years. |
| `inverter_warranty_years`| `inverter_warranty_years`| All | Number (Integer)| `7` | Inverter replacement manufacturer warranty in years. |
| `battery_warranty_years`| `battery_warranty_years`| Off-Grid, Hybrid | Number (Integer)| `5` | Battery manufacturer replacement warranty in years. |
| `payment_terms` | `payment_terms` | All | Dropdown | `Option 1` | `Option 1` (90/10) or `Option 2` (70/25/5). |
| `delivery_time` | `delivery_time` | All | String | `3 weeks` | Project commissioning SLA timeline (Dt). Default: 3 weeks. |
| `transportation_cost`| `transportation_cost`| All | Dropdown | `Included` | `Included`, `Extra`, or `Extra at actuals`. |
| `civil_work_toggle` | `civil_work_toggle` | All | Boolean Toggle | `true` | When true, includes civil foundations in vendor scope. |

---

### Section 5: Exact Mathematical Calculations (Code Reference)

```javascript
// 1. Basic Cost & Composite GST (1.089 factor)
const cost = Number(values.project_cost_inr) || 0;
const basicCost = Math.round(cost / 1.089);
const gst = cost - basicCost;

// 2. Net Payable to Customer (incorporating Subsidy, Additional Cost, and Discount)
const subsidy = Number(values.subsidy_inr) || 0;
const addCost = Number(values.additional_cost_inr) || 0;
const discount = Number(values.discount_inr) || 0;
const totalCost = cost + addCost;
const netCost = totalCost - subsidy - discount;

// 3. Solar Energy Yield
const capacity = Number(values.min_cumulative_capacity_kwp || values.capacity_kw) || 0;
const yieldFactor = Number(values.specific_yield) || 4.2;
const annualEnergy = Math.round(capacity * yieldFactor * 365);
const monthlyEnergy = Math.round(annualEnergy / 12);

// 4. Utility Savings
const tariff = Number(values.tariff_rs_unit) || 8.0;
const monthlySavings = Math.round(monthlyEnergy * tariff);
const annualSavings = Math.round(annualEnergy * tariff);

// 5. 25-Year Compound Financial Projection
let savings25Yr = 0;
let currentEnergy = annualEnergy * 0.98; // Year 1: 2% initial degradation
let currentTariff = tariff;

for (let year = 1; year <= 25; year++) {
    savings25Yr += Math.round(currentEnergy * currentTariff);
    currentEnergy *= (1 - 0.0055); // 0.55% annual degradation
    currentTariff *= 1.03;         // 3.00% annual tariff escalation
}

// 6. Battery Storage Sizing
const volts = Number(values.battery_voltage) || 0;
const ah = Number(values.battery_ah) || 0;
const packs = Number(values.battery_packs) || 1;
const batteryCapacityKwh = Number((volts * ah * packs / 1000).toFixed(2));
```
"""

# =========================================================================
# 4. 02_Variable_Positions_And_Specs/PDF_VARIABLE_COORDINATES_MAP.md
# =========================================================================
coords_map_md = """# EffiSol Solar Proposal Studio — PDF Variable Coordinates Map
## Exact Geometric Positions, Whiteout Boxes, Fonts, and Colors (72 DPI Points)

> **Coordinate System Note:**  
> All coordinates are measured in standard PDF points (1/72 inch) using the **bottom-left origin** $(0, 0)$.  
> Page Dimensions: Standard A4 Portrait = `595.28` pt wide by `841.89` pt high.

---

### 1. ON-GRID PROPOSAL (6-PAGE MASTER TEMPLATE)

#### Page 1: Cover Page (`pages[0]`)
| Element / Variable | Whiteout Rect `[x, y, w, h]` | Fill Color | Text Pos `[x, y]` | Font Family | Size | Text Color | Alignment / Formatting |
|:---|:---|:---|:---|:---|:---|:---|:---|
| **Cover Title Banner** | `[35, 608, 540, 46]` | `#0B5394` (Blue) | Centered, `y: 624` | Helvetica-Bold | 16 (auto-fit 520) | `#FFFFFF` | Format: `"{capacity} kW {type} ON-Grid Solar PV System"` |
| **Cover Subtitle Line** | N/A (Wiped by banner)| N/A | OMITTED | N/A | N/A | N/A | Client Comment: Completely omitted |
| **Customer Name** | `[80, 334, 452, 28]` | `#FFFFFF` (White) | Centered, `y: 341` | Helvetica-Bold | 18 (auto-fit 420) | `#000000` | Format: Raw customer name |
| **Cover Logo (Bottom Left)** | `[40, 555, 275, 632]` (fitz) | `#FFFFFF` | `[45, 569.5, 210, 49.1]` | Image | N/A | N/A | New official EffiSol RGBA logo |

#### Pages 2 & 3: Project Showcases 1 & 2 (`pages[1]` & `pages[2]`)
- **Top Header Banner Logo:** Patched at `fitz.Rect(38, 21.1, 213, 62.0)` with new EffiSol RGBA logo. Surrounding text (`MNRE Channel Partner`, etc.) 100% intact.
- **Page 3 Experience Badge:** Microscopic whiteout at `fitz.Rect(63.8, 690.5, 72.5, 701.5)`. Digit `'9'` inserted at `Point(64.2, 700.5)` with `segoeuib.ttf` at size 9.2. All 6 photos 100% sharp.

#### Page 4: System Summary & Financial Benefits (`pages[3]`)
| Element / Variable | Whiteout Rect `[x, y, w, h]` | Fill Color | Text Pos `[x, y]` | Font Family | Size | Text Color | Alignment / Formatting |
|:---|:---|:---|:---|:---|:---|:---|:---|
| **Summary Header Title** | `[30, 644, 555, 21]` | `#FFFFFF` | Centered, `y: 648.5` | Helvetica-Bold | 15 (auto-fit 500) | `#000000` | Format: `"{capacity} kW OnGrid Solar PV System Summary"` |
| **System Details Subhead** | `[37, 590, 265, 16]` | `#FFFFFF` | `[37.7, 594.0]` | Helvetica-Bold | 12 | `#0B5394` | Format: `"{capacity} kW On Grid Solar PV System"` |
| **Cumulative Capacity** | `[185, 521, 120, 15]` | `#FFFFFF` | `[187.4, 524.5]` | Helvetica-Bold | 12 | `#000000` | Format: `"{min_cumulative_capacity_kwp} kWp"` |
| **Panel Technology** | `[135, 504, 170, 15]` | `#FFFFFF` | `[137.2, 507.2]` | Helvetica-Bold | 11 (auto-fit 165) | `#000000` | Format: `"{tech} Bifacial {category} Solar"` |
| **Panel Wattage** | `[68, 487, 235, 15]` | `#FFFFFF` | `[69.2, 490.2]` | Helvetica | 11 | `#000000` | Format: `"Panels {wattage} W or above"` |
| **Panel Brand** | `[108, 471.5, 195, 15]` | `#FFFFFF` | `[110.3, 475.0]` | Helvetica | 11 (auto-fit 190) | `#000000` | Format: `"{panel_brand}"` |
| **Inverter Capacity** | `[68, 420.5, 235, 15]` | `#FFFFFF` | `[69.2, 424.0]` | Helvetica-Bold | 11 | `#0B5394` | Format: `"{inverter_capacity_kva} kW On Grid Inverter"` |
| **Inverter Brand** | `[108, 404, 195, 15]` | `#FFFFFF` | `[110.3, 407.5]` | Helvetica | 11 (auto-fit 190) | `#000000` | Format: `"{inverter_brand}"` |
| **Structure Type** | `[65, 334, 238, 32]` | `#FFFFFF` | `[67.0, 348.0]` | Helvetica-Bold | 10 (auto-fit 235) | `#000000` | Format: `"{structure_type}"` |
| **Project Cost** | `[391, 552.5, 194, 16]`| `#FFFFFF` | `[394.0, 556.0]` | Helvetica-Bold | 12 | `#000000` | Format: `"Rs. {formatINR(project_cost)}"` |
| **Additional Cost Note** | `[310, 458, 280, 36]` | `#FFFFFF` | `[312.0, 476.0]` | Helvetica-Bold | 9.5 (auto-fit 275)| `#C81E1E` (Red) | If AC > 0: `Note: {ACn}: Rs. {formatINR(AC)}` |
| **Government Subsidy** | `[474, 433.5, 114, 16]`| `#FFFFFF` | `[476.6, 436.5]` | Helvetica-Bold | 12 | `#E16A09` (Orange)| Format: `"Rs. {formatINR(subsidy)}"` |
| **Net Cost to Customer** | `[453, 404, 135, 16]` | `#FFFFFF` | `[455.6, 407.5]` | Helvetica-Bold | 13 | `#007832` (Green) | Format: `"Rs. {formatINR(netCost)}"` |
| **Annual Energy Output** | `[390, 278, 130, 18]` | `#FFFFFF` | `[396.0, 281.5]` | Helvetica | 12 | `#000000` | Format: `"{formatINR(annualEnergy)} units"` |
| **Monthly Energy Output** | `[354, 253, 110, 15]` | `#FFFFFF` | `[356.9, 256.2]` | Helvetica | 12 | `#000000` | Format: `"{formatINR(monthlyEnergy)} units"` |
| **Monthly Bill Savings** | `[395, 218, 110, 15]` | `#FFFFFF` | `[397.7, 221.0]` | Helvetica-Bold | 12 | `#000000` | Format: `"{formatINR(monthlySavings)}"` |
| **Annual Bill Savings** | `[389, 198, 110, 15]` | `#FFFFFF` | `[391.1, 201.2]` | Helvetica-Bold | 12 | `#000000` | Format: `"{formatINR(annualSavings)}"` |
| **Tariff Rate Footnote** | `[525, 180, 55, 14]` | `#FFFFFF` | `[527.3, 183.0]` | Helvetica | 10 | `#000000` | Format: `"Rs. {tariff}/unit)"` |
| **25-Year Total Savings** | `[393, 148.5, 130, 16]`| `#FFFFFF` | `[394.9, 152.0]` | Helvetica-Bold | 12 | `#004B87` (Blue) | Format: `"{formatINR(savings25Yr)}"` |

#### Page 5: Commercial Offer & Schedule of Prices (`pages[4]`)
| Element / Variable | Whiteout Rect `[x, y, w, h]` | Fill Color | Text Pos `[x, y]` | Font Family | Size | Text Color | Alignment / Formatting |
|:---|:---|:---|:---|:---|:---|:---|:---|
| **Commercial Header Title** | `[75, 530, 385, 24]` | `#FFFFFF` | `[78.3, 536.5]` | Helvetica-Bold | 13 (auto-fit 380) | `#000000` | Format: `"{capacity} kW OnGrid Solar PV system"` |
| **Basic Price (Excl GST)** | `[474, 530, 106, 24]` | `#FFFFFF` | `[478.7, 536.5]` | Helvetica-Bold | 12 | `#000000` | Format: `"Rs. {formatINR(basicCost)}"` |
| **Cumulative Capacity** | `[358, 474, 110, 15]` | `#FFFFFF` | `[361.2, 477.5]` | Helvetica-Bold | 12 | `#000000` | Format: `"{min_cumulative_capacity_kwp} kWp"` |
| **Panel Technology** | `[280, 458.5, 190, 15]`| `#FFFFFF` | `[283.9, 462.0]` | Helvetica-Bold | 12 (auto-fit 185) | `#000000` | Format: `"{tech} Bifacial {category} Solar"` |
| **Panel Wattage** | `[172, 444, 298, 15]` | `#FFFFFF` | `[174.5, 447.5]` | Helvetica-Bold | 12 | `#000000` | Format: `"{wattage} Wp or above"` |
| **Panel Brand** | `[171, 429, 299, 15]` | `#FFFFFF` | `[173.1, 432.5]` | Helvetica-Bold | 12 (auto-fit 295) | `#000000` | Format: `"{panel_brand}"` |
| **Inverter Rating** | `[252, 400, 218, 15]` | `#FFFFFF` | `[255.2, 403.5]` | Helvetica-Bold | 12 (auto-fit 214) | `#000000` | `"{capacity} kVA Inverter"` ("3 phase" removed) |
| **Inverter Brand** | `[173, 385.5, 297, 15]`| `#FFFFFF` | `[175.2, 389.0]` | Helvetica-Bold | 12 (auto-fit 293) | `#000000` | Format: `"{inverter_brand}"` |
| **Structure Type** | `[135, 312, 335, 28]` | `#FFFFFF` | `[137.4, 320.0]` | Helvetica-Bold | 11 (auto-fit 330) | `#000000` | Format: `"{structure_type}"` |
| **GST Amount** | `[474, 106, 106, 19]` | `#FFFFFF` | `[478.7, 112.5]` | Helvetica-Bold | 12 | `#000000` | Format: `"Rs. {formatINR(gst)}"` |
| **Total Price** | `[474, 81, 106, 15]` | `#FFFFFF` | `[478.7, 84.5]` | Helvetica-Bold | 13 | `#000000` | Format: `"Rs. {formatINR(project_cost)}"` |
| **Net Payable Banner** | `[466.7, 52.5, 116.3, 27]`| `#0B5394` (Blue) | `[481.9, 62.7]` | Helvetica-Bold | 14 | `#FFFFFF` | Format: `"Rs. {formatINR(netCost)}"` |
| **Additional Cost Note**| `[35, 28, 540, 22]` | `#FFFFFF` | `[36.2, 35.0]` | Helvetica-Bold | 10.5 (auto-fit 530)| `#C81E1E` (Red) | If AC > 0: `Note : “{ACn}” : Rs. {formatINR(AC)}` |

#### Page 6: Terms & Conditions (`pages[5]`)
| Element / Variable | Whiteout Rect `[x, y, w, h]` | Fill Color | Text Pos `[x, y]` | Font Family | Size | Text Color | Alignment / Formatting |
|:---|:---|:---|:---|:---|:---|:---|:---|
| **Turnkey Scope (Row 2)** | `[300, 595, 285, 16]` | `#FFFFFF` | `[301.0, 600.0]` | Helvetica-Bold | 9.5 | `#000000` | "Price for Detailed design, Installation and commissioning Included" |
| **Product Warranty Pw1** | `[330, 542, 250, 14]` | `#FFFFFF` | `[337.0, 546.0]` | Helvetica-Bold | 9.5 | `#000000` | `"•  {panel_warranty_years} years Product warranty"` |
| **Performance Warranty Pw2**| `[330, 500, 250, 42]` | `#FFFFFF` | `[337.0, 528.0]` | Helvetica-Bold | 9.5 | `#000000` | `"•  {panel_performance_warranty_years} years Performance warranty"` |
| **Inverter Warranty** | `[330, 477, 250, 15]` | `#FFFFFF` | `[337.0, 480.5]` | Helvetica-Bold | 9.5 | `#000000` | `"•  {inverter_warranty_years} years manufacturer warranty for Grid-tie inverters"` (with space) |
| **Payment Terms (Row 5)** | `[295, 375, 290, 95]` | `#FFFFFF` | Multi-line `y: 457.0` | Helvetica / Bold | 9.0 / 9.5 | `#000000` | Option 1 (90/10) or Option 2 (70/25/5) |
| **Delivery Time Dt (Row 6)**| `[295, 245, 290, 45]` | `#FFFFFF` | Multi-line `y: 278.0` | Helvetica | 9.0 | `#000000` | `"Within {delivery_time} from date of PO..."` |
| **Transportation Cost** | `[300, 226, 150, 16]` | `#FFFFFF` | `[301.0, 230.5]` | Helvetica-Bold | 9.5 | `#000000` | `"{transportation_cost}"` (Included / Extra / Extra at actuals) |
| **Civil Work Client Scope** | `[300, 140, 200, 14]` | `#FFFFFF` | N/A (Whiteout only)| N/A | N/A | N/A | Wiped if `civil_work_toggle === false` |
| **Offer Valid Date** | `[298, 124, 120, 17]` | `#FFFFFF` | `[301.0, 127.5]` | Helvetica-Bold | 10 | `#000000` | Format: `DD-MM-YYYY` |

---

### 2. OFF-GRID PROPOSAL (8-PAGE / 6-PAGE TEMPLATE)

- **Cover Page (`pages[0]`):** Banner Wipe `[31, 610, 561, 56]`, Text `y: 636`, Prepared For `[80, 275, 452, 142]`, Text `y: 373`, Submitted To `y: 318`.
- **Specs & Dynamic Load Table (`pages[3]`):** Table body wipe `[34, 368, 555, 219]`, Dynamic rows starting `y: 587.0`, columns `[128.1, 79.5, 68.9, 130.6, 143.3]`, Daily Energy `[275, 337, 85, 20]`, System Spec bullets `[28, 136, 554, 96]`.
- **Backup Duration Table (`pages[4]`):** Body wipe `[30, 50, 555, 592]`, Header banner `[38, 602, 536, 36]` in `#0B579D`, 10 load steps (1hr down to 15hr) calculated as `battCap * 0.9 * 0.9 * factor`.
- **Commercial Offer (`pages[5]`):** Component block `[96, 290, 388, 180]`, Basic Price `[491, 492, 97, 22]`, GST `[491, 88, 97, 16]`, Total `[491, 70.5, 97, 14]`, Discount lines `[33, yBottom, 557.4, ...]`.
- **Terms & Conditions (`pages[6]`):** Inverter warranty `[325, 511, 14, 12]`, Battery warranty `[335, 476, 12, 12]`, Civil work `[317, 195, 250, 21]`, Offer Valid `[300, 173, 140, 16]`.

---

### 3. SMART HYBRID PROPOSAL (7-PAGE / 5-PAGE TEMPLATE)

- **Cover Page (`pages[0]`):** Techno-Commercial Banner `[31.5, 610, 560, 130.5]`, Prepared For `[50, 390, 512, 190]`, Submitted To `y: 495`, Company Footer `[335, 165, 250, 145]`.
- **Proposed System (`pages[3]`):** Panel capacity `[50, 495, 500, 20]`, Inverter capacity `[50, 468, 500, 20]`, LiFePO4 battery `[75, 412, 480, 24]`.
- **Summary & Benefits (`pages[4]`):** Header `[30, 640, 550, 40]`, Left Specs Column `[40, 247, 283, 360]`, Right Pricing Column `[326, 310, 264, 230]`, 25-Year Diesel Savings `[150, 135, 330, 18]`.
- **Commercial Offer (`pages[5]`):** Header `[92, 569, 380, 22]`, Basic Cost `[480, 567, 94, 24]`, Components Schedule `[92, 357, 380, 183]`, GST `[480, 137, 94, 22]`, Total `[480, 100.5, 94, 26.5]`.
- **Terms & Conditions (`pages[6]`):** Inverter warranty `[312, 444, 24, 18]`, Battery warranty `[315, 404, 17, 18]`, Delivery time `[300, 182, 270, 16]`, Civil work `[45, 102, 250, 16]`, Offer valid `[300, 62, 120, 18]`.
"""

# =========================================================================
# 5. 02_Variable_Positions_And_Specs/variable_coordinates_map.json
# =========================================================================
coords_json_data = {
    "system_units": "PDF Points (1/72 inch), Origin: Bottom-Left (0,0)",
    "page_dimensions": {"width": 595.28, "height": 841.89, "format": "A4 Portrait"},
    "branding_coordinates": {
        "cover_page_logo": {"wipe_rect": [40, 555, 275, 632], "insert_rect": [45, 569.5, 255, 618.6], "asset": "effisol_logo_tight_rgba.png"},
        "header_banner_logo": {"wipe_rect": [35, 2, 225, 80], "insert_rect": [38, 21.1, 213, 62.0], "asset": "effisol_logo_tight_rgba.png"},
        "page_3_experience_patch": {"wipe_rect": [63.8, 690.5, 72.5, 701.5], "text_point": [64.2, 700.5], "char": "9", "font": "segoeuib.ttf", "size": 9.2}
    },
    "ongrid_6page": {
        "page_1_cover": {
            "title_banner_rect": {"x": 35, "y": 608, "width": 540, "height": 46, "color": [11, 83, 148]},
            "title_text": {"y": 624, "font": "Helvetica-Bold", "size": 16, "max_width": 520, "color": [255, 255, 255], "align": "center"},
            "customer_name_rect": {"x": 80, "y": 334, "width": 452, "height": 28, "color": [255, 255, 255]},
            "customer_name_text": {"y": 341, "font": "Helvetica-Bold", "size": 18, "max_width": 420, "color": [0, 0, 0], "align": "center"}
        },
        "page_4_summary": {
            "summary_title": {"rect": [30, 644, 555, 21], "text_pos": ["center", 648.5], "font": "Helvetica-Bold", "size": 15, "color": [0, 0, 0]},
            "system_subhead": {"rect": [37, 590, 265, 16], "text_pos": [37.7, 594.0], "font": "Helvetica-Bold", "size": 12, "color": [11, 83, 148]},
            "cumulative_capacity": {"rect": [185, 521, 120, 15], "text_pos": [187.4, 524.5], "font": "Helvetica-Bold", "size": 12, "color": [0, 0, 0]},
            "panel_technology": {"rect": [135, 504, 170, 15], "text_pos": [137.2, 507.2], "font": "Helvetica-Bold", "size": 11, "color": [0, 0, 0]},
            "panel_wattage": {"rect": [68, 487, 235, 15], "text_pos": [69.2, 490.2], "font": "Helvetica", "size": 11, "color": [0, 0, 0]},
            "panel_brand": {"rect": [108, 471.5, 195, 15], "text_pos": [110.3, 475.0], "font": "Helvetica", "size": 11, "color": [0, 0, 0]},
            "inverter_capacity": {"rect": [68, 420.5, 235, 15], "text_pos": [69.2, 424.0], "font": "Helvetica-Bold", "size": 11, "color": [11, 83, 148]},
            "inverter_brand": {"rect": [108, 404, 195, 15], "text_pos": [110.3, 407.5], "font": "Helvetica", "size": 11, "color": [0, 0, 0]},
            "structure_type": {"rect": [65, 334, 238, 32], "text_pos": [67.0, 348.0], "font": "Helvetica-Bold", "size": 10, "color": [0, 0, 0]},
            "project_cost": {"rect": [391, 552.5, 194, 16], "text_pos": [394.0, 556.0], "font": "Helvetica-Bold", "size": 12, "color": [0, 0, 0]},
            "additional_cost_note": {"rect": [310, 458, 280, 36], "text_pos": [312.0, 476.0], "font": "Helvetica-Bold", "size": 9.5, "color": [200, 30, 30]},
            "subsidy": {"rect": [474, 433.5, 114, 16], "text_pos": [476.6, 436.5], "font": "Helvetica-Bold", "size": 12, "color": [225, 106, 9]},
            "net_cost": {"rect": [453, 404, 135, 16], "text_pos": [455.6, 407.5], "font": "Helvetica-Bold", "size": 13, "color": [0, 120, 50]},
            "annual_energy": {"rect": [390, 278, 130, 18], "text_pos": [396.0, 281.5], "font": "Helvetica", "size": 12, "color": [0, 0, 0]},
            "monthly_energy": {"rect": [354, 253, 110, 15], "text_pos": [356.9, 256.2], "font": "Helvetica", "size": 12, "color": [0, 0, 0]},
            "monthly_savings": {"rect": [395, 218, 110, 15], "text_pos": [397.7, 221.0], "font": "Helvetica-Bold", "size": 12, "color": [0, 0, 0]},
            "annual_savings": {"rect": [389, 198, 110, 15], "text_pos": [391.1, 201.2], "font": "Helvetica-Bold", "size": 12, "color": [0, 0, 0]},
            "tariff_note": {"rect": [525, 180, 55, 14], "text_pos": [527.3, 183.0], "font": "Helvetica", "size": 10, "color": [0, 0, 0]},
            "savings_25yr": {"rect": [393, 148.5, 130, 16], "text_pos": [394.9, 152.0], "font": "Helvetica-Bold", "size": 12, "color": [0, 75, 135]}
        },
        "page_5_commercial": {
            "title": {"rect": [75, 530, 385, 24], "text_pos": [78.3, 536.5], "font": "Helvetica-Bold", "size": 13, "color": [0, 0, 0]},
            "basic_cost": {"rect": [474, 530, 106, 24], "text_pos": [478.7, 536.5], "font": "Helvetica-Bold", "size": 12, "color": [0, 0, 0]},
            "cumulative_capacity": {"rect": [358, 474, 110, 15], "text_pos": [361.2, 477.5], "font": "Helvetica-Bold", "size": 12, "color": [0, 0, 0]},
            "panel_tech": {"rect": [280, 458.5, 190, 15], "text_pos": [283.9, 462.0], "font": "Helvetica-Bold", "size": 12, "color": [0, 0, 0]},
            "panel_wattage": {"rect": [172, 444, 298, 15], "text_pos": [174.5, 447.5], "font": "Helvetica-Bold", "size": 12, "color": [0, 0, 0]},
            "panel_brand": {"rect": [171, 429, 299, 15], "text_pos": [173.1, 432.5], "font": "Helvetica-Bold", "size": 12, "color": [0, 0, 0]},
            "inverter_capacity": {"rect": [252, 400, 218, 15], "text_pos": [255.2, 403.5], "font": "Helvetica-Bold", "size": 12, "color": [0, 0, 0]},
            "inverter_brand": {"rect": [173, 385.5, 297, 15], "text_pos": [175.2, 389.0], "font": "Helvetica-Bold", "size": 12, "color": [0, 0, 0]},
            "structure_type": {"rect": [135, 312, 335, 28], "text_pos": [137.4, 320.0], "font": "Helvetica-Bold", "size": 11, "color": [0, 0, 0]},
            "gst_amount": {"rect": [474, 106, 106, 19], "text_pos": [478.7, 112.5], "font": "Helvetica-Bold", "size": 12, "color": [0, 0, 0]},
            "total_price": {"rect": [474, 81, 106, 15], "text_pos": [478.7, 84.5], "font": "Helvetica-Bold", "size": 13, "color": [0, 0, 0]},
            "net_payable_banner": {"rect": [466.7, 52.5, 116.3, 27], "text_pos": [481.9, 62.7], "font": "Helvetica-Bold", "size": 14, "color": [255, 255, 255], "bg": [11, 83, 148]},
            "additional_cost_note": {"rect": [35, 28, 540, 22], "text_pos": [36.2, 35.0], "font": "Helvetica-Bold", "size": 10.5, "color": [200, 30, 30]}
        },
        "page_6_terms": {
            "turnkey_scope": {"rect": [300, 595, 285, 16], "text_pos": [301.0, 600.0], "font": "Helvetica-Bold", "size": 9.5, "color": [0, 0, 0]},
            "module_product_warranty": {"rect": [330, 542, 250, 14], "text_pos": [337.0, 546.0], "font": "Helvetica-Bold", "size": 9.5, "color": [0, 0, 0]},
            "module_performance_warranty": {"rect": [330, 500, 250, 42], "text_pos": [337.0, 528.0], "font": "Helvetica-Bold", "size": 9.5, "color": [0, 0, 0]},
            "inverter_warranty": {"rect": [330, 477, 250, 15], "text_pos": [337.0, 480.5], "font": "Helvetica-Bold", "size": 9.5, "color": [0, 0, 0]},
            "payment_terms": {"rect": [295, 375, 290, 95], "text_pos": [301.0, 457.0], "font": "Helvetica-Bold", "size": 9.5, "color": [0, 0, 0]},
            "delivery_time": {"rect": [295, 245, 290, 45], "text_pos": [301.0, 278.0], "font": "Helvetica", "size": 9.0, "color": [0, 0, 0]},
            "transportation_cost": {"rect": [300, 226, 150, 16], "text_pos": [301.0, 230.5], "font": "Helvetica-Bold", "size": 9.5, "color": [0, 0, 0]},
            "civil_work_scope": {"rect": [300, 140, 200, 14]},
            "offer_valid_date": {"rect": [298, 124, 120, 17], "text_pos": [301.0, 127.5], "font": "Helvetica-Bold", "size": 10, "color": [0, 0, 0]}
        }
    }
}

# Write text files to package directory
with open(os.path.join(DOCS_DIR, "MASTER_PROJECT_DOCUMENTATION.md"), "w", encoding="utf-8") as f:
    f.write(master_doc)

with open(os.path.join(DOCS_DIR, "HOW_TO_TRAIN_AND_BUILD_FROM_SCRATCH_IN_ONE_RUN.md"), "w", encoding="utf-8") as f:
    f.write(ai_guide)

with open(os.path.join(VARS_DIR, "VARIABLE_DICTIONARY_AND_FORMULAS.md"), "w", encoding="utf-8") as f:
    f.write(var_dict_md)

with open(os.path.join(VARS_DIR, "PDF_VARIABLE_COORDINATES_MAP.md"), "w", encoding="utf-8") as f:
    f.write(coords_map_md)

with open(os.path.join(VARS_DIR, "variable_coordinates_map.json"), "w", encoding="utf-8") as f:
    json.dump(coords_json_data, f, indent=4)

print("Documentation and coordinate files written successfully.")

# Copy Tagged and Template PDFs
pdf_files_to_copy = [
    "EffiSol_Solar_Proposal_TAGGED (1).pdf",
    "EffiSol_Solar_Proposal_TAGGED.pdf",
    "5.5 kW  Solar Proposal for  Mr. Rama Krishna  (1).pdf",
    "5 kW Off-grid Solar PV System for Mr. K. Rama Rao.pdf",
    "template_ongrid_6page.pdf",
    "clean_offgrid_8page_template.pdf",
    "clean_hybrid_7page_template.pdf",
    "effisol_logo_new.png",
    "effisol_logo_tight_rgba.png"
]

for pdf in pdf_files_to_copy:
    src = os.path.join(BASE_DIR, pdf)
    if os.path.exists(src):
        dst = os.path.join(PDFS_DIR, pdf)
        shutil.copyfile(src, dst)
        print(f"Copied {pdf} -> {dst}")
    else:
        print(f"Notice: {pdf} not found in root, skipping.")

# Copy Source Code and Scripts
code_files_to_copy = [
    "app.html",
    "index.html",
    "template_pdf.js",
    "template_offgrid_pdf.js",
    "template_hybrid_pdf.js",
    "pdf-lib.min.js",
    "build_complete_app.py",
    "rebuild_perfect_template.py",
    "patch_all_templates_and_logos.py",
    "encode_all_template_js.py",
    "create_deployment_zip.py",
    "robots.txt"
]

for code in code_files_to_copy:
    src = os.path.join(BASE_DIR, code)
    if os.path.exists(src):
        dst = os.path.join(CODE_DIR, code)
        shutil.copyfile(src, dst)
        print(f"Copied {code} -> {dst}")
    else:
        print(f"Notice: {code} not found in root, skipping.")

# Create a master README in the package root
pkg_readme = f"""# EffiSol Solar Proposal Studio — Complete Master Archive & Documentation
Generated for: EffiSol Energy Solutions Pvt. Ltd.

This folder contains the complete, unabridged documentation, original tagged PDFs, clean vector templates, exact variable coordinates (Markdown and JSON), and the full production source code.

## Folder Contents:
1. `01_Documentation/`
   - `MASTER_PROJECT_DOCUMENTATION.md`: Complete story, architecture, 17-point client audit report, and errors & recovery guide.
   - `HOW_TO_TRAIN_AND_BUILD_FROM_SCRATCH_IN_ONE_RUN.md`: Deterministic blueprint and AI prompt to generate this entire app in one single shot.
2. `02_Variable_Positions_And_Specs/`
   - `VARIABLE_DICTIONARY_AND_FORMULAS.md`: Complete dictionary of all 17 inputs, outputs, mathematical calculations, and financial models.
   - `PDF_VARIABLE_COORDINATES_MAP.md`: Human-readable table of every coordinate, whiteout rect, font size, and color (72 DPI points).
   - `variable_coordinates_map.json`: Machine-readable JSON coordinate tree ready for automated ingestion.
3. `03_Tagged_And_Template_PDFs/`
   - `EffiSol_Solar_Proposal_TAGGED (1).pdf`: The original tagged reference document with visual placeholders.
   - `5.5 kW  Solar Proposal for  Mr. Rama Krishna  (1).pdf`: The original high-res customer quotation.
   - `5 kW Off-grid Solar PV System for Mr. K. Rama Rao.pdf`: The original off-grid reference proposal.
   - `template_ongrid_6page.pdf`: The clean 6-page On-Grid vector template with new logo and 9 years experience.
   - `clean_offgrid_8page_template.pdf`: The clean 8-page Off-Grid vector template.
   - `clean_hybrid_7page_template.pdf`: The clean 7-page Hybrid vector template.
   - `effisol_logo_new.png` & `effisol_logo_tight_rgba.png`: Official company branding graphics.
4. `04_Source_Code_And_Scripts/`
   - `app.html` & `index.html`: Production single-page web app with all modes, live math, and direct access.
   - `template_pdf.js`, `template_offgrid_pdf.js`, `template_hybrid_pdf.js`: Modular Base64 vector template streams.
   - `pdf-lib.min.js`: Client-side WebAssembly PDF engine.
   - `build_complete_app.py`: Master compiler script that synthesizes the entire application.
   - `patch_all_templates_and_logos.py`: Surgical vector template and logo patching script.
   - `encode_all_template_js.py`: Fast base64 encoder script.
   - `create_deployment_zip.py`: Packaging and artifact distribution utility.
"""

with open(os.path.join(PKG_DIR, "README.md"), "w", encoding="utf-8") as f:
    f.write(pkg_readme)

# Also copy README.md to root workspace
with open(os.path.join(BASE_DIR, "README.md"), "w", encoding="utf-8") as f:
    f.write(pkg_readme)

# Create Master Zip Archive
zip_path = os.path.join(BASE_DIR, "EffiSol_Master_Documentation_And_Assets.zip")
print(f"Creating master zip archive at {zip_path}...")
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for root, dirs, files in os.walk(PKG_DIR):
        for f in files:
            full_path = os.path.join(root, f)
            arcname = os.path.relpath(full_path, BASE_DIR)
            z.write(full_path, arcname=arcname)
            print(f"Zipped: {arcname}")

zip_size = os.path.getsize(zip_path)
print(f"Zip created: {zip_size:,} bytes ({zip_size / (1024*1024):.2f} MB)")

# Copy Zip to Brain Artifact directory
artifact_dir = r"C:\Users\user\.gemini\antigravity\brain\4752c12d-4d52-424e-83b8-bb4ec66c8218"
artifact_dest = os.path.join(artifact_dir, "EffiSol_Master_Documentation_And_Assets.zip")
shutil.copyfile(zip_path, artifact_dest)
print(f"Copied master zip to brain artifact: {artifact_dest}")
