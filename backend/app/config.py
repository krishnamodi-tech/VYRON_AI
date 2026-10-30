import os
from pathlib import Path
from pydantic import BaseModel
from dotenv import load_dotenv

# Search for .env in current dir, parent dir, or root
env_paths = [
    Path.cwd() / ".env",
    Path(__file__).resolve().parent.parent / ".env",
    Path(__file__).resolve().parent.parent.parent / ".env",
]
for p in env_paths:
    if p.exists():
        load_dotenv(p)
        break

class Settings(BaseModel):
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # Open-Weight AI Inference (Preferred for Best Open-Source AI Track)
    # Compatible with Groq, vLLM, Ollama, OpenRouter
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "").strip()
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile").strip()
    OPENAI_API_BASE: str = os.getenv("OPENAI_API_BASE", "https://api.groq.com/openai/v1").strip()

    # Google Gemini Fallback/Alternative
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "").strip()
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash").strip()

    MAX_UPLOAD_SIZE_MB: int = int(os.getenv("MAX_UPLOAD_SIZE_MB", "15"))
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS", "*")

    @property
    def has_groq_key(self) -> bool:
        return bool(self.GROQ_API_KEY and not self.GROQ_API_KEY.startswith("your_"))

    @property
    def has_gemini_key(self) -> bool:
        return bool(self.GEMINI_API_KEY and not self.GEMINI_API_KEY.startswith("your_"))

    @property
    def active_provider(self) -> str:
        if self.has_groq_key:
            return "groq"
        if self.has_gemini_key:
            return "gemini"
        return "hybrid"

settings = Settings()
