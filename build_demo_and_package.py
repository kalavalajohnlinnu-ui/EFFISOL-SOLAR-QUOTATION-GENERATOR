import os
import subprocess
import shutil

print("1. Extracting original sources...")
with open('build_complete_app.py', 'r', encoding='utf-8') as f:
    py_code = f.read()

start_marker = "html_content = r'''"
start_idx = py_code.find(start_marker)
end_marker = "'''"
end_idx = py_code.find(end_marker, start_idx + len(start_marker))

raw_html = py_code[start_idx + len(start_marker):end_idx]

# Extract styles
style_start = raw_html.find('<style>')
style_end = raw_html.find('</style>', style_start)
base_css = raw_html[style_start + len('<style>'):style_end].strip()

# Extract shield & main script
shield_start = raw_html.find('<script>')
shield_end = raw_html.find('</script>', shield_start)
base_shield = raw_html[shield_start + len('<script>'):shield_end].strip()

main_script_start = raw_html.rfind('<script>')
main_script_end = raw_html.rfind('</script>')
base_main_js = raw_html[main_script_start + len('<script>'):main_script_end].strip()

print(f"Base CSS: {len(base_css)} chars, Base JS: {len(base_main_js)} chars.")

# =========================================================================
# 2. CREATE DEMO CSS (WITH KJL WATERMARK & BADGE)
# =========================================================================
demo_css = base_css + """

/* =========================================================================
   KJL DEMO WATERMARK & SECURITY STYLING
   ========================================================================= */
.kjl-watermark-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    pointer-events: none;
    z-index: 9990;
    background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='280' height='180' viewBox='0 0 280 180'><text x='50%' y='50%' fill='rgba(255,255,255,0.038)' font-family='sans-serif' font-weight='800' font-size='24' text-anchor='middle' transform='rotate(-25 140 90)'>KJL DEMO</text></svg>");
}

.kjl-demo-badge {
    position: fixed;
    top: 14px;
    right: 20px;
    z-index: 9995;
    background: linear-gradient(135deg, rgba(239, 68, 68, 0.22), rgba(245, 158, 11, 0.22));
    border: 1px solid rgba(239, 68, 68, 0.45);
    color: #fca5a5;
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 1px;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.45);
    display: flex;
    align-items: center;
    gap: 8px;
    pointer-events: none;
}

.kjl-demo-badge::before {
    content: '';
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #ef4444;
    box-shadow: 0 0 10px #ef4444;
    animation: kjlPulse 2s infinite;
}

@keyframes kjlPulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.4; transform: scale(0.85); }
}

.kjl-permanently-blurred {
    filter: blur(35px) grayscale(100%) !important;
    pointer-events: none !important;
    user-select: none !important;
}
"""

with open('demo_style.css', 'w', encoding='utf-8') as f:
    f.write(demo_css)
print("Saved demo_style.css")

# =========================================================================
# 3. CREATE DEMO JS (WITH TAMPER ENGINE & PDF WATERMARK)
# =========================================================================
# In the PDF generators, we want to stamp "KJL DEMO VERSION" on each page
pdf_watermark_hook = """
// KJL Demo Watermark Generator Hook
try {
    if (typeof pdfDoc !== 'undefined' && pdfDoc && pdfDoc.getPages) {
        const pages = pdfDoc.getPages();
        for (let _pi = 0; _pi < pages.length; _pi++) {
            const _cp = pages[_pi];
            const { width: _pw, height: _ph } = _cp.getSize();
            _cp.drawText('KJL DEMO VERSION', {
                x: _pw / 2 - 170,
                y: _ph / 2,
                size: 40,
                color: pdfLibObj.rgb(0.82, 0.22, 0.22),
                opacity: 0.16,
                rotate: pdfLibObj.degrees(45),
            });
        }
    }
} catch(_err) {}
"""

# Replace all occurrences of "const pdfBytes = await pdfDoc.save();"
modified_main_js = base_main_js.replace(
    "const pdfBytes = await pdfDoc.save();",
    pdf_watermark_hook + "\n                const pdfBytes = await pdfDoc.save();"
)

# Active Tamper Engine for Demo
tamper_engine_js = """
// =========================================================================
// KJL HARDENED ACTIVE TAMPER-DETECTION & PERMANENT LOCKOUT ENGINE
// =========================================================================
(function() {
    'use strict';

    function triggerPermanentLock(reason) {
        try {
            localStorage.setItem('_0xkjl_lock', 'LOCKED_PERMANENT');
            sessionStorage.setItem('_0xkjl_lock', 'LOCKED_PERMANENT');
            document.cookie = "_0xkjl_lock=LOCKED_PERMANENT; path=/; max-age=31536000";
        } catch(e) {}

        // Apply heavy permanent blur immediately to viewport
        try {
            document.body.classList.add('kjl-permanently-blurred');
            document.documentElement.classList.add('kjl-permanently-blurred');
        } catch(e) {}

        setTimeout(function() {
            document.documentElement.innerHTML = `
                <head>
                    <meta charset="UTF-8">
                    <title>ACCESS PERMANENTLY TERMINATED</title>
                    <style>
                        body {
                            margin: 0;
                            padding: 24px;
                            background: #040711;
                            color: #ef4444;
                            font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                            display: flex;
                            flex-direction: column;
                            align-items: center;
                            justify-content: center;
                            min-height: 100vh;
                            box-sizing: border-box;
                            text-align: center;
                        }
                        .lock-icon {
                            font-size: 4.5rem;
                            margin-bottom: 16px;
                            filter: drop-shadow(0 0 30px rgba(239, 68, 68, 0.8));
                        }
                        h1 {
                            font-size: 2.2rem;
                            color: #f87171;
                            margin: 0 0 12px;
                            font-weight: 800;
                            letter-spacing: 1.5px;
                        }
                        p {
                            color: #94a3b8;
                            max-width: 540px;
                            font-size: 1.1rem;
                            line-height: 1.6;
                            margin: 0 0 28px;
                        }
                        .seal {
                            font-size: 0.82rem;
                            color: #fca5a5;
                            background: rgba(239, 68, 68, 0.12);
                            border: 1px solid rgba(239, 68, 68, 0.35);
                            padding: 10px 24px;
                            border-radius: 8px;
                            font-family: monospace;
                            letter-spacing: 1px;
                        }
                    </style>
                </head>
                <body>
                    <div class="lock-icon">🛑</div>
                    <h1>DEMO TERMINAL PERMANENTLY LOCKED</h1>
                    <p>
                        Unauthorized Developer Tools or Source inspection was detected on this device.<br>
                        In accordance with KJL security policies, this demo build has been permanently disabled.
                    </p>
                    <div class="seal">SECURITY ID: KJL-BUILD-TAMPER-REVOKED</div>
                </body>
            `;
            window.stop && window.stop();
        }, 30);
    }

    // 1. Allow author/client reset via ?reset_kjl_lock=1
    try {
        if (window.location.search && window.location.search.indexOf('reset_kjl_lock=1') !== -1) {
            localStorage.removeItem('_0xkjl_lock');
            sessionStorage.removeItem('_0xkjl_lock');
            document.cookie = "_0xkjl_lock=; path=/; max-age=0";
        }
    } catch(e) {}

    // Check if already permanently locked
    try {
        if (localStorage.getItem('_0xkjl_lock') === 'LOCKED_PERMANENT' ||
            sessionStorage.getItem('_0xkjl_lock') === 'LOCKED_PERMANENT' ||
            document.cookie.indexOf('_0xkjl_lock=LOCKED_PERMANENT') !== -1) {
            triggerPermanentLock('STORED_LOCK');
            return;
        }
    } catch(e) {}

    // 2. Window outer vs inner disparity check (Docked DevTools detection)
    // Safe threshold prevents false positives from standard browser chrome + Windows DPI scaling
    function checkWindowDiff() {
        if (window.outerWidth > 768) {
            const widthDiff = (window.outerWidth - window.innerWidth) > 320;
            const heightDiff = (window.outerHeight - window.innerHeight) > 340;
            if (widthDiff || heightDiff) {
                triggerPermanentLock('DOCK_RESIZE');
            }
        }
    }
    window.addEventListener('resize', checkWindowDiff);
    setInterval(checkWindowDiff, 1000);

    // 2b. Sources tab / Debugger execution tripwire (Instant lock on DevTools Sources)
    setInterval(function() {
        var t0 = Date.now();
        (function() { debugger; })();
        var t1 = Date.now();
        if (t1 - t0 > 100) {
            triggerPermanentLock('SOURCES_DEBUGGER_TRIGGER');
        }
    }, 1000);

    // 3. Console Evaluation & Inspection Getter Trap
    const trapElem = document.createElement('div');
    Object.defineProperty(trapElem, 'id', {
        get: function() {
            triggerPermanentLock('CONSOLE_GETTER');
            return 'kjl';
        }
    });
    setInterval(function() {
        try {
            console.log('%c', trapElem);
            console.clear();
        } catch(e) {}
    }, 900);

    // 4. Keyboard Shortcuts Interceptor (F12, Ctrl+Shift+I/J/C, Ctrl+U, Ctrl+S)
    window.addEventListener('keydown', function(e) {
        if (
            e.keyCode === 123 || 
            (e.ctrlKey && e.shiftKey && (e.keyCode === 73 || e.keyCode === 74 || e.keyCode === 67)) || 
            (e.ctrlKey && (e.keyCode === 85 || e.keyCode === 83)) ||
            (e.metaKey && e.altKey && (e.keyCode === 73 || e.keyCode === 74 || e.keyCode === 67)) ||
            (e.metaKey && (e.keyCode === 85 || e.keyCode === 83))
        ) {
            e.preventDefault();
            e.stopImmediatePropagation();
            triggerPermanentLock('KEY_TRIGGER');
            return false;
        }
    }, true);

    // 5. Context menu block & inspection tripwire
    document.addEventListener('contextmenu', function(e) {
        e.preventDefault();
        e.stopImmediatePropagation();
        return false;
    }, true);

    // 6. Execution Latency / Debugger Tripwire
    let lastTick = Date.now();
    setInterval(function() {
        const now = Date.now();
        if (now - lastTick > 350) {
            triggerPermanentLock('TIMING_LATENCY');
        }
        lastTick = now;
    }, 120);

    window._kjlTriggerLock = triggerPermanentLock;
})();
"""

combined_demo_js = base_shield + "\n\n" + tamper_engine_js + "\n\n" + modified_main_js
with open('temp_unobfuscated_demo.js', 'w', encoding='utf-8') as f:
    f.write(combined_demo_js)

print("Obfuscating demo_script.js with javascript-obfuscator...")
cmd = [
    'npx.cmd', 'javascript-obfuscator',
    'temp_unobfuscated_demo.js',
    '--output', 'demo_script.js',
    '--compact', 'true',
    '--control-flow-flattening', 'true',
    '--control-flow-flattening-threshold', '0.75',
    '--dead-code-injection', 'true',
    '--string-array', 'true',
    '--string-array-encoding', 'base64',
    '--string-array-threshold', '0.8',
    '--split-strings', 'true',
    '--disable-console-output', 'true',
    '--source-map', 'false'
]
res = subprocess.run(cmd, capture_output=True, text=True, shell=True)
if res.returncode != 0:
    print("Obfuscator warning, falling back to basic:", res.stderr)
    cmd_basic = ['npx.cmd', 'javascript-obfuscator', 'temp_unobfuscated_demo.js', '--output', 'demo_script.js', '--compact', 'true', '--string-array', 'true', '--string-array-encoding', 'base64']
    subprocess.run(cmd_basic, check=True, shell=True)

if os.path.exists('temp_unobfuscated_demo.js'):
    os.remove('temp_unobfuscated_demo.js')

print(f"demo_script.js generated successfully ({os.path.getsize('demo_script.js')} bytes).")

# =========================================================================
# 4. BUILD DEMO.HTML
# =========================================================================
# Construct demo.html using clean structure
# Pre-render check at line 1 of <head>
prerender_head_check = """
    <!-- Instant Pre-Render Hardcoded Tamper Check -->
    <script>
    (function() {
        try {
            if (localStorage.getItem('_0xkjl_lock') === 'LOCKED_PERMANENT' ||
                sessionStorage.getItem('_0xkjl_lock') === 'LOCKED_PERMANENT' ||
                document.cookie.indexOf('_0xkjl_lock=LOCKED_PERMANENT') !== -1) {
                document.documentElement.innerHTML = '<div style="position:fixed;inset:0;background:#040711;color:#ef4444;font-family:sans-serif;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:24px;z-index:99999999;"><div style="font-size:4rem;margin-bottom:16px;">🛑</div><h1 style="font-size:2rem;color:#f87171;margin:0 0 12px;font-weight:800;">DEMO TERMINAL PERMANENTLY LOCKED</h1><p style="color:#94a3b8;max-width:500px;line-height:1.6;margin:0 0 24px;">Unauthorized Developer Tools or Source inspection was detected on this device.<br>This demo build has been permanently disabled.</p><div style="font-size:0.8rem;color:#fca5a5;border:1px solid rgba(239,68,68,0.3);background:rgba(239,68,68,0.1);padding:8px 20px;border-radius:6px;font-family:monospace;">SECURITY ID: KJL-BUILD-TAMPER-REVOKED</div></div>';
                window.stop && window.stop();
            }
        } catch(e) {}
    })();
    </script>
"""

# In raw_html, remove shield script from head
html_no_shield = raw_html[:shield_start] + prerender_head_check + raw_html[shield_end + len('</script>'):]

# Replace style tag with demo_style.css
style_start_new = html_no_shield.find('<style>')
style_end_new = html_no_shield.find('</style>', style_start_new)
html_with_link = html_no_shield[:style_start_new] + '<link rel="stylesheet" href="demo_style.css">' + html_no_shield[style_end_new + len('</style>'):]

# Add watermark overlay & badge right after <body>
body_idx = html_with_link.find('<body>') + len('<body>')
watermark_html = """
    <!-- KJL Demo Watermark Overlay & Floating Badge -->
    <div class="kjl-watermark-overlay"></div>
    <div class="kjl-demo-badge">KJL • DEMO VERSION</div>
"""
html_with_watermark = html_with_link[:body_idx] + watermark_html + html_with_link[body_idx:]

# Replace last script with demo_script.js
last_script_start = html_with_watermark.rfind('<script>')
last_script_end = html_with_watermark.rfind('</script>')
demo_html = html_with_watermark[:last_script_start] + '<script src="pdf-lib.min.js" defer></script>\n    <script src="demo_script.js" defer></script>' + html_with_watermark[last_script_end + len('</script>'):]

with open('demo.html', 'w', encoding='utf-8') as f:
    f.write(demo_html)
print(f"demo.html generated successfully ({len(demo_html)} chars).")

print("All Demo assets created successfully!")
