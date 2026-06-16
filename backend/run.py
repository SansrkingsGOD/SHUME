#!/usr/bin/env python3
"""
AI Resume & Portfolio Builder — Quick Start
Run: python3 run.py
Then open: frontend/index.html in your browser
"""
import sys, subprocess, os

print("=" * 52)
print("   AI Resume & Portfolio Builder — Starting Up")
print("=" * 52)

# Install deps if missing
try:
    import fastapi, uvicorn, reportlab, docx, sklearn
    print("✅ All dependencies found")
except ImportError as e:
    print(f"📦 Installing missing packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "--break-system-packages", "-q"])
    print("✅ Dependencies installed")

print("🚀 Starting API server on http://localhost:8000")
print("🌐 Open frontend/index.html in your browser")
print("   Press Ctrl+C to stop\n")

os.chdir(os.path.dirname(os.path.abspath(__file__)))
import uvicorn
uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
