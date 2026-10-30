"""
VYRON AI 2.0 — Backend Server Entry Point
Run with: python main.py or py main.py
"""
import sys
import os
from pathlib import Path

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

backend_path = Path(__file__).resolve().parent / "backend"
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

import uvicorn
from app.config import settings

if __name__ == "__main__":
    print("=" * 65)
    print("       🚀 VYRON AI 2.0 — MULTILINGUAL PUBLIC INTELLIGENCE")
    print("=" * 65)
    print(f"[VYRON] Host: http://{settings.HOST}:{settings.PORT}")
    if settings.has_groq_key:
        print(f"[VYRON] AI Engine: OPEN-WEIGHT GROQ ({settings.GROQ_MODEL})")
    elif settings.has_gemini_key:
        print(f"[VYRON] AI Engine: GOOGLE GEMINI ({settings.GEMINI_MODEL})")
    else:
        print(f"[VYRON] AI Engine: HYBRID MODE (Real Direct Translation + Heuristics)")
    print("=" * 65)
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=False)
