import zipfile
import os
import shutil

files_to_pack = [
    # Production Files (Untouched)
    'index.html',
    'style.css',
    'script1.js',
    'app.html',
    
    # Demo Files (With KJL Watermark & Permanent Tamper Engine)
    'demo.html',
    'demo_style.css',
    'demo_script.js',
    
    # PDF Templates & Engines
    'template_pdf.js',
    'template_offgrid_pdf.js',
    'template_hybrid_pdf.js',
    'pdf-lib.min.js',
    'effisol_logo_new.png',
    'effisol_logo_tight_rgba.png',
    
    # Deployment & Caching Configs
    'robots.txt',
    '_headers',
    'netlify.toml',
    
    # Local Server Scripts
    'serve_portal.py',
    'start_portal.bat'
]

zip_name = 'EffiSol_Solar_Quotation_Portal_Complete_With_KJL_Demo.zip'

with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for f in files_to_pack:
        if os.path.exists(f):
            z.write(f, arcname=f)
            size = os.path.getsize(f)
            print(f"Added {f} ({size:,} bytes)")
        else:
            print(f"WARNING: {f} not found!")

total_zip_size = os.path.getsize(zip_name)
print(f"\nCreated {zip_name}: {total_zip_size:,} bytes ({total_zip_size/(1024*1024):.2f} MB)")

# Also copy to effisol_solar_quote_deployment.zip for backward compatibility
shutil.copyfile(zip_name, 'effisol_solar_quote_deployment.zip')

artifact_dir = r"C:\Users\user\.gemini\antigravity\brain\4752c12d-4d52-424e-83b8-bb4ec66c8218"
artifact_dest = os.path.join(artifact_dir, zip_name)
shutil.copyfile(zip_name, artifact_dest)
shutil.copyfile(zip_name, os.path.join(artifact_dir, 'effisol_solar_quote_deployment.zip'))
print(f"Copied deployment zip to artifact: {artifact_dest}")
