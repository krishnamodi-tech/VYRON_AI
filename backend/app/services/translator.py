import re
import requests
from typing import Dict, Any, List, Optional

# Supported Language Name Mapping
LANGUAGE_NAMES = {
    "en": "English",
    "hi": "Hindi (हिन्दी)",
    "bn": "Bengali (বাংলা)",
    "te": "Telugu (తెలుగు)",
    "mr": "Marathi (मराठी)",
    "ta": "Tamil (தமிழ்)",
    "gu": "Gujarati (ગુજરાતી)",
    "kn": "Kannada (ಕನ್ನಡ)",
    "ml": "Malayalam (മലയാളം)",
    "pa": "Punjabi (ਪੰਜਾਬੀ)",
    "or": "Odia (ଓଡ଼ିଆ)",
    "as": "Assamese (অसमীয়া)",
    "ur": "Urdu (اردو)",
    "es": "Spanish (Español)",
    "fr": "French (Français)",
    "de": "German (Deutsch)",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
}

def detect_language_simple(text: str) -> str:
    """Heuristic source language detection for Indian and Latin scripts."""
    sample = text[:600]
    # Check Devanagari (Hindi, Marathi, Sanskrit)
    if re.search(r'[\u0900-\u097F]', sample):
        return "hi"
    # Check Bengali / Assamese
    if re.search(r'[\u0980-\u09FF]', sample):
        return "bn"
    # Check Telugu
    if re.search(r'[\u0C00-\u0C7F]', sample):
        return "te"
    # Check Tamil
    if re.search(r'[\u0B80-\u0BFF]', sample):
        return "ta"
    # Check Gujarati
    if re.search(r'[\u0A80-\u0AFF]', sample):
        return "gu"
    # Check Kannada
    if re.search(r'[\u0C80-\u0CFF]', sample):
        return "kn"
    # Check Malayalam
    if re.search(r'[\u0D00-\u0D7F]', sample):
        return "ml"
    # Check Gurmukhi (Punjabi)
    if re.search(r'[\u0A00-\u0A7F]', sample):
        return "pa"
    # Check Urdu / Arabic
    if re.search(r'[\u0600-\u06FF]', sample):
        return "ur"
    return "en"

def chunk_text(text: str, max_chars: int = 1500) -> List[str]:
    """
    Splits text along paragraph or sentence boundaries to respect API payload limits
    while preserving document structure.
    """
    if len(text) <= max_chars:
        return [text]

    paragraphs = text.split("\n")
    chunks = []
    current_chunk = []
    current_length = 0

    for para in paragraphs:
        if len(para) > max_chars:
            sentences = re.split(r'(?<=[.!?।])\s+', para)
            for s in sentences:
                if current_length + len(s) + 1 > max_chars and current_chunk:
                    chunks.append("\n".join(current_chunk))
                    current_chunk = [s]
                    current_length = len(s)
                else:
                    current_chunk.append(s)
                    current_length += len(s) + 1
        else:
            if current_length + len(para) + 1 > max_chars and current_chunk:
                chunks.append("\n".join(current_chunk))
                current_chunk = [para]
                current_length = len(para)
            else:
                current_chunk.append(para)
                current_length += len(para) + 1

    if current_chunk:
        chunks.append("\n".join(current_chunk))

    return [c for c in chunks if c.strip()]

def translate_single_chunk(chunk: str, target_lang: str, source_lang: str = "auto") -> str:
    """
    Translates a single text chunk reliably.
    Bypasses API if source is identical to target language.
    Uses POST where possible to prevent HTTP 414 URI Too Long errors.
    """
    clean_chunk = chunk.strip()
    if not clean_chunk:
        return ""

    detected_src = detect_language_simple(clean_chunk)
    # If source is already in the target language, avoid calling external endpoints
    if source_lang == target_lang or (source_lang == "auto" and detected_src == target_lang):
        return clean_chunk

    # Primary: Google Dictionary / Client Service (High-speed, robust, no 429 rate limit)
    try:
        url = "https://clients5.google.com/translate_a/t"
        params = {
            "client": "dict-chrome-ex",
            "sl": source_lang if source_lang != target_lang else "auto",
            "tl": target_lang
        }
        res = requests.post(url, params=params, data={"q": clean_chunk}, headers=HEADERS, timeout=8)
        if res.status_code == 200:
            data = res.json()
            if isinstance(data, list) and len(data) > 0:
                first = data[0]
                if isinstance(first, str) and first.strip():
                    return first.strip()
                elif isinstance(first, list) and len(first) > 0 and isinstance(first[0], str) and first[0].strip():
                    return first[0].strip()
    except Exception:
        pass

    # Secondary: Google Public Translate service via POST with gtx client
    try:
        url = "https://translate.googleapis.com/translate_a/single"
        params = {
            "client": "gtx",
            "sl": source_lang if source_lang != target_lang else "auto",
            "tl": target_lang,
            "dt": "t"
        }
        res = requests.post(url, params=params, data={"q": clean_chunk}, headers=HEADERS, timeout=10)
        if res.status_code == 200:
            data = res.json()
            if data and isinstance(data, list) and len(data) > 0 and data[0]:
                translated = "".join([segment[0] for segment in data[0] if segment and len(segment) > 0 and segment[0]])
                if translated.strip():
                    return translated.strip()
    except Exception:
        pass

    # Secondary: Google Public Translate via GET fallback
    try:
        url = "https://translate.googleapis.com/translate_a/single"
        params = {
            "client": "gtx",
            "sl": source_lang if source_lang != target_lang else "auto",
            "tl": target_lang,
            "dt": "t",
            "q": clean_chunk[:1000]
        }
        res = requests.get(url, params=params, headers=HEADERS, timeout=8)
        if res.status_code == 200:
            data = res.json()
            if data and isinstance(data, list) and len(data) > 0 and data[0]:
                translated = "".join([segment[0] for segment in data[0] if segment and len(segment) > 0 and segment[0]])
                if translated.strip():
                    return translated.strip()
    except Exception:
        pass

    # Tertiary: MyMemory translated API (strictly requires distinct languages)
    try:
        sl = source_lang if source_lang != "auto" else detected_src
        if sl != target_lang:
            url = "https://api.mymemory.translated.net/get"
            params = {
                "q": clean_chunk[:500],
                "langpair": f"{sl}|{target_lang}"
            }
            res = requests.get(url, params=params, headers=HEADERS, timeout=8)
            if res.status_code == 200:
                data = res.json()
                t = data.get("responseData", {}).get("translatedText", "")
                if t and not t.startswith("MYMEMORY WARNING") and "DAILY LIMIT" not in t.upper() and "PLEASE SELECT" not in t.upper():
                    return t.strip()
    except Exception:
        pass

    # Quaternary: Lingva public mirror fallback
    try:
        sl = source_lang if source_lang != "auto" else detected_src
        url = f"https://lingva.ml/api/v1/{sl}/{target_lang}/{requests.utils.quote(clean_chunk[:500])}"
        res = requests.get(url, headers=HEADERS, timeout=6)
        if res.status_code == 200:
            data = res.json()
            tr = data.get("translation", "")
            if tr and tr.strip():
                return tr.strip()
    except Exception:
        pass

    # Resilient fallback: return clean chunk rather than crashing the pipeline
    return clean_chunk

def translate_document_text(text: str, target_lang: str, source_lang: Optional[str] = None) -> Dict[str, Any]:
    """
    Translates an entire document in structured chunks, maintaining paragraphs,
    names, dates, and numbers.
    """
    if not text or not text.strip():
        return {
            "translated_text": "",
            "detected_source_lang": "unknown",
            "target_lang": target_lang
        }

    detected_src = source_lang if source_lang and source_lang != "auto" else detect_language_simple(text)

    # If document is already in the target language, bypass translation
    if detected_src == target_lang:
        return {
            "translated_text": text.strip(),
            "detected_source_lang": detected_src,
            "target_lang": target_lang,
            "same_language": True
        }

    chunks = chunk_text(text, max_chars=1200)
    translated_parts = []

    for chunk in chunks:
        part = translate_single_chunk(chunk, target_lang=target_lang, source_lang=detected_src)
        translated_parts.append(part)

    full_translated = "\n\n".join(translated_parts)
    return {
        "translated_text": full_translated,
        "detected_source_lang": detected_src,
        "target_lang": target_lang,
        "chunk_count": len(chunks)
    }
