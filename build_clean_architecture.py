import os
import re
import subprocess
import shutil

print("1. Reading build_complete_app.py...")
with open('build_complete_app.py', 'r', encoding='utf-8') as f:
    py_code = f.read()

# Extract html_content from build_complete_app.py
start_marker = "html_content = r'''"
end_marker = "'''\n\n# Obfuscate"
start_idx = py_code.find(start_marker)
end_idx = py_code.find(end_marker)

if start_idx == -1 or end_idx == -1:
    # Try finding alternative end marker
    end_marker = "'''"
    start_idx = py_code.find(start_marker)
    end_idx = py_code.find(end_marker, start_idx + len(start_marker))

raw_html = py_code[start_idx + len(start_marker):end_idx]
print(f"Extracted raw_html length: {len(raw_html)} characters.")

# Locate parts:
# 1. Shield script in <head>
shield_start = raw_html.find('<script>')
shield_end = raw_html.find('</script>', shield_start)
shield_code = raw_html[shield_start + len('<script>'):shield_end].strip()
print(f"Extracted shield code: {len(shield_code)} characters.")

# 2. Styles in <style>
style_start = raw_html.find('<style>')
style_end = raw_html.find('</style>', style_start)
style_code = raw_html[style_start + len('<style>'):style_end].strip()
print(f"Extracted style code: {len(style_code)} characters.")

# 3. Main script at bottom
main_script_start = raw_html.rfind('<script>')
main_script_end = raw_html.rfind('</script>')
main_script_code = raw_html[main_script_start + len('<script>'):main_script_end].strip()
print(f"Extracted main script code: {len(main_script_code)} characters.")

# Combine shield_code and main_script_code
combined_js = shield_code + "\n\n" + main_script_code
with open('temp_unobfuscated_bundle.js', 'w', encoding='utf-8') as f:
    f.write(combined_js)

print("2. Obfuscating combined JavaScript bundle with javascript-obfuscator...")
# Run javascript-obfuscator
cmd = [
    'npx.cmd', 'javascript-obfuscator',
    'temp_unobfuscated_bundle.js',
    '--output', 'script1.js',
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
    print("Obfuscator error:", res.stderr)
    # Fallback to basic obfuscation if advanced flags fail
    cmd_basic = ['npx.cmd', 'javascript-obfuscator', 'temp_unobfuscated_bundle.js', '--output', 'script1.js', '--compact', 'true', '--string-array', 'true', '--string-array-encoding', 'base64']
    subprocess.run(cmd_basic, check=True, shell=True)

with open('script1.js', 'r', encoding='utf-8') as f:
    obfuscated_js = f.read()

print(f"Obfuscated script1.js successfully ({len(obfuscated_js)} characters).")

# Clean style.css
with open('style.css', 'w', encoding='utf-8') as f:
    f.write(style_code)
print(f"Wrote style.css successfully ({len(style_code)} characters).")

# Build index.html (EXACTLY like Pick 2: references style.css and script1.js, zero inline scripts in head)
# Remove the shield <script>...</script> from head
html_no_shield = raw_html[:shield_start] + raw_html[shield_end + len('</script>'):]

# Replace <style>...</style> with <link rel="stylesheet" href="style.css">
style_start_new = html_no_shield.find('<style>')
style_end_new = html_no_shield.find('</style>', style_start_new)
html_with_link = html_no_shield[:style_start_new] + '<link rel="stylesheet" href="style.css">' + html_no_shield[style_end_new + len('</style>'):]

# Replace last <script>...</script> with <script src="script1.js"></script>
last_script_start = html_with_link.rfind('<script>')
last_script_end = html_with_link.rfind('</script>')
index_html = html_with_link[:last_script_start] + '<script src="pdf-lib.min.js" defer></script>\n    <script src="script1.js" defer></script>' + html_with_link[last_script_end + len('</script>'):]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(index_html)
print(f"Wrote index.html successfully ({len(index_html)} characters).")

# Build standalone app.html (all-in-one with zero plaintext scripts in <head>)
# In app.html, the shield is NOT in <head> (it's bundled in the obfuscated script at the bottom)
app_html = raw_html[:shield_start] + raw_html[shield_end + len('</script>'):]
last_start_app = app_html.rfind('<script>')
last_end_app = app_html.rfind('</script>')
app_html = app_html[:last_start_app + len('<script>')] + '\n' + obfuscated_js + '\n' + app_html[last_end_app:]

with open('app.html', 'w', encoding='utf-8') as f:
    f.write(app_html)
print(f"Wrote app.html successfully ({len(app_html)} characters).")

# Remove temp file
if os.path.exists('temp_unobfuscated_bundle.js'):
    os.remove('temp_unobfuscated_bundle.js')

print("All builds completed successfully!")
