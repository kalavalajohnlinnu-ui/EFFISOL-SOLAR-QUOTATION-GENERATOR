import zipfile
import os
import shutil

files_to_pack = [
    # Production Files ONLY (Clean, unbloated, secure)
    'index.html',
    'style.css',
    'script1.js',
    'telemetry.js',
    
    # Dedicated Owner CRM & Admin Command Center
    'admin.html',
    'admin.css',
    'admin.js',
    
    # PDF Templates & High-Speed In-Memory Engine
    'template_pdf.js',
    'template_offgrid_pdf.js',
    'template_hybrid_pdf.js',
    'pdf-lib.min.js',
    'effisol_logo_new.png',
    'effisol_logo_tight_rgba.png',
    
    # Security Headers, CSP & Caching Configs
    'robots.txt',
    '_headers',
    'netlify.toml'
]

zip_names = [
    'effisol_solar_portal_netlify.zip',
    'EffiSol_Solar_Quotation_Portal_Production.zip'
]

for zip_name in zip_names:
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

    artifact_dir = r"C:\Users\user\.gemini\antigravity\brain\4752c12d-4d52-424e-83b8-bb4ec66c8218"
    artifact_dest = os.path.join(artifact_dir, zip_name)
    shutil.copyfile(zip_name, artifact_dest)
    print(f"Copied {zip_name} to artifact: {artifact_dest}")
