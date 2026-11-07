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

# 2. Styles in <style>
style_start = raw_html.find('<style>')
style_end = raw_html.find('</style>', style_start)
style_code = raw_html[style_start + len('<style>'):style_end].strip()

# 3. Main script at bottom
main_script_start = raw_html.rfind('<script>')
main_script_end = raw_html.rfind('</script>')
main_script_code = raw_html[main_script_start + len('<script>'):main_script_end].strip()

# Combine shield_code and main_script_code
combined_js = shield_code + "\n\n" + main_script_code
with open('temp_unobfuscated_bundle.js', 'w', encoding='utf-8') as f:
    f.write(combined_js)

print("2. Obfuscating combined JavaScript bundle with javascript-obfuscator...")
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
    cmd_basic = ['npx.cmd', 'javascript-obfuscator', 'temp_unobfuscated_bundle.js', '--output', 'script1.js', '--compact', 'true', '--string-array', 'true', '--string-array-encoding', 'base64']
    subprocess.run(cmd_basic, check=True, shell=True)

with open('script1.js', 'r', encoding='utf-8') as f:
    obfuscated_js = f.read()

print(f"Obfuscated script1.js successfully ({len(obfuscated_js)} characters).")

# Clean style.css
with open('style.css', 'w', encoding='utf-8') as f:
    f.write(style_code)
print(f"Wrote style.css successfully ({len(style_code)} characters).")

# Build index.html
html_no_shield = raw_html[:shield_start] + raw_html[shield_end + len('</script>'):]
style_start_new = html_no_shield.find('<style>')
style_end_new = html_no_shield.find('</style>', style_start_new)
html_with_link = html_no_shield[:style_start_new] + '<link rel="stylesheet" href="style.css">' + html_no_shield[style_end_new + len('</style>'):]

last_script_start = html_with_link.rfind('<script>')
last_script_end = html_with_link.rfind('</script>')
scripts_bundle = '''    <!-- High-Speed In-Memory PDF Engine & Instant Proposal Templates -->
    <script src="pdf-lib.min.js"></script>
    <script src="template_pdf.js"></script>
    <script src="template_offgrid_pdf.js"></script>
    <script src="template_hybrid_pdf.js"></script>
    <script src="script1.js"></script>'''

index_html = html_with_link[:last_script_start] + scripts_bundle + html_with_link[last_script_end + len('</script>'):]
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(index_html)
print(f"Wrote index.html successfully ({len(index_html)} characters).")

# Clean up temp bundle
if os.path.exists('temp_unobfuscated_bundle.js'):
    os.remove('temp_unobfuscated_bundle.js')

print("All clean architecture builds completed successfully (app.html excluded)!")
