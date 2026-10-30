import time
from typing import Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .config import settings
from .services.extractor import extract_text_from_pdf, validate_text_input, ExtractionError
from .services.translator import translate_document_text
from .services.ai_engine import VyronAIEngine
from .services.cache import cost_optimizer

app = FastAPI(
    title="VYRON AI Explainer — Open-Weight Backend API",
    description="Multilingual Public Document Simplifier, Jargon Decoder & Grounded Q&A Platform",
    version="2.0.0"
)

# 1. Security Headers Middleware (Addresses Browser Security / Suspicious Site Warnings)
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response: Response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(self)"
    return response

# 2. CORS Middleware with spec-compliant credentials handling
raw_origins = [o.strip() for o in settings.CORS_ORIGINS.split(",") if o.strip()]
if not raw_origins or "*" in raw_origins:
    origins = ["*"]
    allow_creds = False
else:
    origins = raw_origins
    allow_creds = True

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=allow_creds,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Initialize AI Engine (Prioritizes Open-Weight Groq / Llama 3.3 / Qwen, then Gemini)
if settings.has_groq_key:
    ai_engine = VyronAIEngine(
        api_key=settings.GROQ_API_KEY,
        model=settings.GROQ_MODEL,
        provider="groq",
        api_base=settings.OPENAI_API_BASE
    )
elif settings.has_gemini_key:
    ai_engine = VyronAIEngine(
        api_key=settings.GEMINI_API_KEY,
        model=settings.GEMINI_MODEL,
        provider="gemini"
    )
else:
    ai_engine = VyronAIEngine(
        api_key="",
        model="Hybrid Fallback Engine",
        provider="hybrid"
    )

start_time = time.time()

# Request Models for JSON Endpoints
class SimplifyMoreRequest(BaseModel):
    paragraph: str
    target_lang: str = "hi"

class ExplainTermRequest(BaseModel):
    term: str
    context: str = ""
    target_lang: str = "hi"

class ChatDocumentRequest(BaseModel):
    document_text: str
    question: str
    target_lang: str = "hi"

class DirectTranslateRequest(BaseModel):
    text: str
    target_lang: str = "hi"
    source_lang: Optional[str] = "auto"

@app.get("/api/health")
async def health_check():
    """Returns real-time backend operational status, credentials presence, and engine mode."""
    return {
        "status": "online",
        "uptime_seconds": int(time.time() - start_time),
        "ai_engine_configured": ai_engine.is_configured,
        "active_model": ai_engine.model if ai_engine.is_configured else "Vyron Hybrid (WASM/Local + Direct Translation)",
        "provider": ai_engine.provider if ai_engine.is_configured else "hybrid_free",
        "features": {
            "open_weight_ai": ai_engine.provider == "groq",
            "pdf_extraction": True,
            "multilingual_translation": True,
            "jargon_decoding": True,
            "document_grounded_chat": True,
            "audio_tts_support": True,
            "interactive_term_explainer": True,
            "zero_token_caching": True
        },
        "token_optimization": cost_optimizer.get_metrics(),
        "max_upload_size_mb": settings.MAX_UPLOAD_SIZE_MB
    }

@app.post("/api/translate")
async def direct_translate(req: DirectTranslateRequest):
    """Faithful standalone translation preserving formatting, names, and numbers."""
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Text required for translation.")
    try:
        result = translate_document_text(req.text, req.target_lang, req.source_lang)
        return {
            "status": "success",
            "original_text": req.text,
            "translated_text": result["translated_text"],
            "target_lang": req.target_lang,
            "detected_source_lang": result["detected_source_lang"]
        }
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc))

@app.post("/api/process-document")
async def process_document(
    text: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    target_lang: str = Form("hi"),
    explanation_level: str = Form("standard")
):
    """
    Multimodal document pipeline:
    1. Ingests raw text or PDF.
    2. Extracts structured content.
    3. Performs Faithful Literal Translation.
    4. Generates Simplified Civic Meaning, Grounded Action Checklist, and Contextual Jargon.
    """
    extracted_text = ""
    metadata = {"source": "text_input"}

    # Handle File Upload
    if file:
        file_bytes = await file.read()
        max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
        if len(file_bytes) > max_bytes:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File exceeds maximum allowed size of {settings.MAX_UPLOAD_SIZE_MB}MB."
            )

        content_type = file.content_type or ""
        filename = (file.filename or "").lower()

        if "pdf" in content_type or filename.endswith(".pdf"):
            try:
                extracted_text, metadata = extract_text_from_pdf(file_bytes)
            except ExtractionError as e:
                raise HTTPException(status_code=400, detail=str(e))
        elif any(img_type in content_type for img_type in ["image", "jpeg", "jpg", "png", "webp"]):
            # For images: client-side OCR (Tesseract.js) sends confirmed text
            if text and text.strip():
                extracted_text = text.strip()
                metadata = {"source": "image_client_ocr", "filename": file.filename}
            else:
                raise HTTPException(
                    status_code=400,
                    detail="Image received. OCR extracted text is required."
                )
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file format ({content_type}). Please upload a PDF or Image (JPG, PNG, WEBP)."
            )
    elif text:
        try:
            extracted_text = validate_text_input(text)
            metadata = {"source": "manual_text"}
        except ExtractionError as e:
            raise HTTPException(status_code=400, detail=str(e))
    else:
        raise HTTPException(
            status_code=400,
            detail="No document text or file provided. Please paste text or upload a document."
        )

    if metadata.get("is_scanned_likely") and len(extracted_text.strip()) < 50:
        raise HTTPException(
            status_code=422,
            detail="Scanned PDF has no selectable text layer. Please use the 'Image Upload' or 'Live Camera' tab for OCR."
        )

    # Check Zero-Token Cache First (Serves recurring public circulars with 0 API tokens in 2ms)
    cached_payload = cost_optimizer.get_analysis(extracted_text, target_lang, explanation_level)
    if cached_payload:
        cached_payload["metadata"] = metadata
        return cached_payload

    # Step 2 & 3: Run Comprehension & Faithful Translation Pipeline
    analysis = ai_engine.analyze_document(
        document_text=extracted_text,
        target_lang=target_lang,
        level=explanation_level
    )

    # If analysis provided a faithful translation, use it; otherwise compute via translation pipeline
    faithful_translation = analysis.get("faithful_translation")
    if not faithful_translation or not faithful_translation.strip():
        try:
            tr_res = translate_document_text(extracted_text[:14000], target_lang)
            faithful_translation = tr_res["translated_text"]
        except Exception:
            faithful_translation = analysis.get("simple_explanation", {}).get("simplified_body", "")

    result_payload = {
        "status": "success",
        "metadata": metadata,
        "original_text": extracted_text,
        "literal_translated_text": faithful_translation,
        "faithful_translation": faithful_translation,
        "target_lang": target_lang,
        "analysis": analysis,
        "cached": False
    }
    cost_optimizer.set_analysis(extracted_text, target_lang, explanation_level, result_payload)
    return result_payload

@app.post("/api/chat-document")
async def chat_document(req: ChatDocumentRequest):
    """
    Feature 3: Ask Vyron Anything About This Document
    Answers questions grounded strictly in the uploaded document.
    """
    if not req.document_text.strip():
        raise HTTPException(status_code=400, detail="Document text required.")
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    # Check Zero-Token Chat Cache
    cached_chat = cost_optimizer.get_chat(req.document_text, req.question, req.target_lang)
    if cached_chat:
        return cached_chat

    result = ai_engine.chat_with_document(
        document_text=req.document_text,
        question=req.question,
        target_lang=req.target_lang
    )
    cost_optimizer.set_chat(req.document_text, req.question, req.target_lang, result)
    return result

@app.post("/api/simplify-more")
async def simplify_more(req: SimplifyMoreRequest):
    """Re-simplifies a confusing paragraph further using everyday analogies."""
    if not req.paragraph.strip():
        raise HTTPException(status_code=400, detail="Paragraph text required.")
    result = ai_engine.simplify_more(req.paragraph, req.target_lang)
    return result

@app.post("/api/explain-term")
async def explain_term(req: ExplainTermRequest):
    """Provides an on-demand contextual explanation for a highlighted word or phrase."""
    if not req.term.strip():
        raise HTTPException(status_code=400, detail="Term required.")
    result = ai_engine.explain_single_term(req.term, req.context, req.target_lang)
    return result

# 3. Mount Frontend Static Files (Eliminates file:// camera locks and mixed-origin blocks)
from pathlib import Path
from starlette.staticfiles import StaticFiles

project_root = Path(__file__).resolve().parent.parent.parent
app.mount("/", StaticFiles(directory=str(project_root), html=True), name="static_frontend")
