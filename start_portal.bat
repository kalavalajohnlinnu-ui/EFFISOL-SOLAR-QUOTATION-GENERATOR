@echo off
title EffiSol Proposal Studio - Secure Server
cd /d "%~dp0"
echo Starting EffiSol Proposal Studio with Netlify-Grade Cache Shield...
python serve_portal.py
pause
