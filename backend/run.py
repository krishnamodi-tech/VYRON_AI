import sys
import os
from pathlib import Path

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

backend_path = Path(__file__).resolve().parent
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

import uvicorn
from app.config import settings

if __name__ == "__main__":
    print(f"[VYRON] Starting Backend Server on http://{settings.HOST}:{settings.PORT}")
    if settings.has_groq_key:
        print(f"[VYRON] AI Engine: OPEN-WEIGHT GROQ ({settings.GROQ_MODEL})")
    elif settings.has_gemini_key:
        print(f"[VYRON] AI Engine: GOOGLE GEMINI ({settings.GEMINI_MODEL})")
    else:
        print(f"[VYRON] AI Engine: HYBRID MODE (Direct Translation + Client OCR)")
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=False)
