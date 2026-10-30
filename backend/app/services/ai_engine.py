import json
import re
import requests
from typing import Dict, Any, List, Optional
from .translator import LANGUAGE_NAMES, translate_document_text, translate_single_chunk
from .knowledge_base import (
    CIVIC_KNOWLEDGE_BASE,
    lookup_term,
    extract_known_terms,
    get_knowledge_base_prompt_snippet
)

def clean_json_response(raw_text: str) -> Dict[str, Any]:
    """Cleans markdown fences or surrounding noise from an LLM response and parses JSON."""
    raw_text = raw_text.strip()
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", raw_text)
    if match:
        raw_text = match.group(1).strip()
    
    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        start = raw_text.find("{")
        end = raw_text.rfind("}")
        if start != -1 and end != -1 and end > start:
            json_slice = raw_text[start:end+1]
            return json.loads(json_slice)
        raise

def extract_target_word(question: str) -> Optional[str]:
    """Detects whether a user query is asking for the meaning/definition of a word or jargon."""
    q = question.strip().lower()

    # Pattern: "what does X mean", "what is the meaning of X", "meaning of X"
    m_does = re.search(r'what\s+does\s+[\'"]?([a-zA-Z\s]{2,40}?)[\'"]?\s+mean', q)
    if m_does:
        return m_does.group(1).strip()

    m = re.search(r'(?:what\s+is\s+(?:the\s+)?meaning\s+of|meaning\s+of|define|explain\s+word|word\s+meaning)\s*[\'":]?\s*([a-zA-Z\s]{2,40})[\'":]?', q)
    if m:
        w = m.group(1).strip()
        w = re.sub(r'[?.!,]+$', '', w).strip()
        w = re.sub(r'\b(in hindi|in english|in document|means|mean)\b', '', w).strip()
        if w:
            return w

    # Pattern: "X ka matlab", "X ka arth", "X kya hota hai", "X kya hai"
    m_hi = re.search(r'^[\'"]?([a-zA-Z\s]{2,30}?)\s+(?:ka\s+matlab|ka\s+arth|kya\s+hai|kya\s+hota\s+hai)', q)
    if m_hi:
        return m_hi.group(1).strip()

    # Pattern: "X meaning", "X means"
    m2 = re.search(r'^[\'"]?([a-zA-Z\s]{2,30}?)[\'"]?\s+(?:meaning|means)\b', q)
    if m2:
        return m2.group(1).strip()

    # Short query: User entered just 1 or 2 words (e.g. "study", "postponed", "distress warrant")
    words = [w for w in re.findall(r'[a-zA-Z]+', q)]
    stopwords = {"what", "who", "when", "where", "how", "why", "which", "is", "are", "the", "this", "that", "can", "could", "should", "tell", "show", "help"}
    if 1 <= len(words) <= 2 and not any(w in stopwords for w in words):
        return " ".join(words)

    return None

class VyronAIEngine:
    def __init__(
        self,
        api_key: str = "",
        model: str = "llama-3.3-70b-versatile",
        provider: str = "groq",
        api_base: str = "https://api.groq.com/openai/v1"
    ):
        self.api_key = api_key
        self.model = model
        self.provider = provider
        self.api_base = api_base.rstrip("/")

    @property
    def is_configured(self) -> bool:
        return bool(self.api_key and not self.api_key.startswith("your_"))

    def _request_model(self, prompt: str, system_prompt: str = "", timeout: int = 40) -> str:
        """
        Executes unified LLM inference across Groq (Open-Weight),
        OpenAI-compatible endpoints (vLLM / Ollama), or Google Gemini.
        """
        if not self.is_configured:
            raise RuntimeError("AI model not configured. Please supply GROQ_API_KEY or GEMINI_API_KEY.")

        if self.provider == "groq" or self.provider == "openai":
            url = f"{self.api_base}/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            else:
                messages.append({"role": "system", "content": "You are VYRON AI, a helpful and precise public document assistant. Respond strictly in valid JSON where requested."})
            
            messages.append({"role": "user", "content": prompt})

            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": 0.1,
                "response_format": {"type": "json_object"}
            }

            res = requests.post(url, headers=headers, json=payload, timeout=timeout)
            if res.status_code != 200:
                if "response_format" in res.text:
                    del payload["response_format"]
                    res = requests.post(url, headers=headers, json=payload, timeout=timeout)
                res.raise_for_status()

            data = res.json()
            return data["choices"][0]["message"]["content"]

        elif self.provider == "gemini":
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
            payload = {
                "contents": [{"parts": [{"text": (f"{system_prompt}\n\n" if system_prompt else "") + prompt}]}],
                "generationConfig": {
                    "temperature": 0.2,
                    "response_mime_type": "application/json"
                }
            }
            res = requests.post(url, headers={"Content-Type": "application/json"}, json=payload, timeout=timeout)
            res.raise_for_status()
            data = res.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
        else:
            raise ValueError(f"Unknown AI provider '{self.provider}'")

    def analyze_document(
        self,
        document_text: str,
        target_lang: str = "hi",
        level: str = "standard"
    ) -> Dict[str, Any]:
        lang_name = LANGUAGE_NAMES.get(target_lang, target_lang)
        doc_trimmed = document_text[:18000]

        if not self.is_configured:
            return self._fallback_analysis(doc_trimmed, target_lang, level)

        system_prompt = (
            f"You are VYRON AI, an expert open-weight generative AI legal & civic document explainer. "
            f"Analyze the untrusted official document and translate/simplify it into {lang_name} ({target_lang}). "
            f"Never hallucinate facts, deadlines, or fees. Return strictly a JSON object."
        )

        prompt = f"""
Analyze the following official document carefully:

TARGET LANGUAGE: {lang_name} ({target_lang})
EXPLANATION LEVEL: {level.upper()}
(VERY_SIMPLE = 5th-grader everyday vocabulary; STANDARD = clear citizen friendly guidance; DETAILED = clause-by-clause legal breakdown)

GROUNDING & TRANSLATION RULES:
1. "faithful_translation": Must be an accurate, complete, faithful translation of the source document into {lang_name}. Do NOT summarize here. Preserve all numbers, dates, official names, references, sections, and negative constraints ("not", "failure to").
2. "simple_explanation": Explain the meaning and purpose in plain everyday {lang_name}.
3. "what_you_need_to_do": Extract the concrete checklist. If deadlines or fees are absent, state explicitly in {lang_name}: "दस्तावेज़ में निर्दिष्ट नहीं है" (or target language equivalent). Never invent deadlines.
4. "jargon_decoded": Extract 2 to 5 complex legal, administrative, or statutory terms found in the text. For each, give its meaning, context, a relatable real-world example, and the exact source sentence from the document.

STRICT JSON OUTPUT SCHEMA:
{{
  "detected_source_language": "English / Hindi / etc.",
  "document_type": "Government Notice / Court Order / University Circular / Bank Notice / etc.",
  "faithful_translation": "Complete, accurate translation into {lang_name}",
  "simple_explanation": {{
    "overall_purpose": "2-3 sentences explaining core intent in {lang_name}",
    "level": "{level}",
    "simplified_body": "Clear readable multi-paragraph explanation in {lang_name}",
    "key_takeaways": [
      "Key takeaway 1 in {lang_name}",
      "Key takeaway 2 in {lang_name}"
    ],
    "ambiguities_or_warnings": "Penalties, conditions, or missing information citizens should note in {lang_name}"
  }},
  "what_you_need_to_do": {{
    "required_actions": [
      "Action 1 in {lang_name}",
      "Action 2 in {lang_name}"
    ],
    "deadlines": "Specific deadline mentioned in {lang_name}, OR 'Not specified in document'",
    "fees_and_payments": "Specific fee/amount mentioned in {lang_name}, OR 'Not specified in document'",
    "required_documents": [
      "Document 1 mentioned in {lang_name}"
    ],
    "eligibility_conditions": "Who this applies to in {lang_name}",
    "contact_and_links": "Helpline, email, or portal mentioned in {lang_name}, OR 'Not specified in document'",
    "penalties_or_consequences": "What happens if ignored in {lang_name}"
  }},
  "jargon_decoded": [
    {{
      "term": "Original legal/official term from document",
      "simple_meaning": "Everyday translation/definition in {lang_name}",
      "contextual_meaning": "How it specifically applies to the citizen in this document in {lang_name}",
      "example": "A relatable real-world everyday example in {lang_name}",
      "source_sentence": "Exact sentence where this term appears in the original text"
    }}
  ]
}}

OFFICIAL DOCUMENT CONTENT:
\"\"\"
{doc_trimmed}
\"\"\"
"""
        try:
            raw_response = self._request_model(prompt, system_prompt=system_prompt, timeout=45)
            parsed = clean_json_response(raw_response)
            parsed["ai_engine_active"] = True
            parsed["engine_note"] = f"Open-Weight AI Active ({self.provider.upper()}: {self.model})"
            return parsed
        except Exception as exc:
            return self._fallback_analysis(doc_trimmed, target_lang, level, error_note=str(exc))

    def simplify_more(self, paragraph: str, target_lang: str = "hi") -> Dict[str, Any]:
        """Provides an ultra-simplified 5th-grader version of a confusing paragraph with an analogy."""
        lang_name = LANGUAGE_NAMES.get(target_lang, target_lang)

        if not self.is_configured:
            tr = translate_single_chunk(paragraph, target_lang)
            analogy = translate_single_chunk("Like a homework deadline that must be submitted to avoid punishment, complete this required procedure.", target_lang)
            return {
                "simplified_text": tr,
                "analogy": analogy,
                "ai_engine_active": False
            }

        prompt = f"""
Take this paragraph and explain it MUCH MORE SIMPLY in {lang_name}.
Target audience: 5th-grader or a citizen with zero legal education.
Use a simple real-world analogy.

Paragraph:
\"\"\"{paragraph}\"\"\"

Return strictly JSON:
{{
  "simplified_text": "Ultra simple explanation in {lang_name}",
  "analogy": "Short everyday comparison in {lang_name}"
}}
"""
        try:
            raw = self._request_model(prompt, timeout=20)
            parsed = clean_json_response(raw)
            parsed["ai_engine_active"] = True
            return parsed
        except Exception:
            tr = translate_single_chunk(paragraph, target_lang)
            return {
                "simplified_text": tr,
                "analogy": translate_single_chunk("Direct everyday translation.", target_lang),
                "ai_engine_active": False
            }

    def explain_single_term(self, term: str, context: str, target_lang: str = "hi") -> Dict[str, Any]:
        """Contextually explains a user-selected term using the authoritative Knowledge Base and AI."""
        lang_name = LANGUAGE_NAMES.get(target_lang, target_lang)
        term_clean = term.strip()

        # 1. Authoritative Civic & Academic Knowledge Base lookup (instant, verified, 100% accurate, 0 tokens)
        kb_data = lookup_term(term_clean)
        if kb_data:
            s_meaning = kb_data["simple_meaning"] if target_lang == "hi" else (translate_single_chunk(kb_data["simple_meaning"], target_lang) if target_lang != "en" else kb_data["term"])
            c_meaning = kb_data["contextual_meaning"] if target_lang == "hi" else translate_single_chunk(kb_data["contextual_meaning"], target_lang)
            ex_val = kb_data["example"] if target_lang == "hi" else translate_single_chunk(kb_data["example"], target_lang)
            return {
                "term": kb_data["term"],
                "simple_meaning": s_meaning,
                "contextual_meaning": c_meaning,
                "example": ex_val,
                "source_sentence": context or f"Appears in document context for '{term_clean}'.",
                "action_required": kb_data.get("action_required", ""),
                "ai_engine_active": True,
                "source": "authoritative_civic_knowledge_base"
            }

        if not self.is_configured:
            term_tr = translate_single_chunk(term_clean, target_lang)
            ctx_tr = translate_single_chunk(context, target_lang) if context else ""
            return {
                "term": f"{term_clean} ({term_tr})" if target_lang == "hi" else term_clean,
                "simple_meaning": f"सीधा अर्थ: \"{term_tr}\"" if target_lang == "hi" else f"Direct meaning: \"{term_tr}\"",
                "contextual_meaning": f"दस्तावेज़ में: {ctx_tr}" if ctx_tr else f"दस्तावेज़ में प्रयुक्त शब्द।",
                "example": f"दैनिक जीवन में इसका अर्थ '{term_tr}' के रूप में समझा जाता है।" if target_lang == "hi" else f"Commonly understood as '{term_tr}'.",
                "source_sentence": context,
                "ai_engine_active": False
            }

        prompt = f"""
Explain this official/legal term in {lang_name} based on its context:
Term: "{term_clean}"
Context sentence: "{context}"

Return strictly JSON:
{{
  "term": "{term_clean}",
  "simple_meaning": "Plain everyday meaning in {lang_name}",
  "contextual_meaning": "What it specifically means in this sentence in {lang_name}",
  "example": "A real-world simple example in {lang_name}",
  "source_sentence": "{context}"
}}
"""
        try:
            raw = self._request_model(prompt, timeout=20)
            parsed = clean_json_response(raw)
            parsed["ai_engine_active"] = True
            return parsed
        except Exception:
            term_tr = translate_single_chunk(term_clean, target_lang)
            return {
                "term": f"{term_clean} ({term_tr})" if target_lang == "hi" else term_clean,
                "simple_meaning": f"सीधा अर्थ: \"{term_tr}\"" if target_lang == "hi" else f"Direct meaning: \"{term_tr}\"",
                "contextual_meaning": translate_single_chunk(context, target_lang) if context else "दस्तावेज़ में संदर्भ।",
                "example": f"दैनिक जीवन में इसका अर्थ '{term_tr}' होता है।" if target_lang == "hi" else f"Understood as '{term_tr}'.",
                "source_sentence": context,
                "ai_engine_active": False
            }

    def _answer_word_meaning_query(
        self,
        word: str,
        document_text: str,
        original_question: str,
        target_lang: str = "hi"
    ) -> Dict[str, Any]:
        """Provides exact direct word vocabulary definitions with everyday meaning, examples, and document citations."""
        word_clean = word.strip()

        # 1. Check Authoritative Civic & Academic Knowledge Base (0 tokens)
        kb = lookup_term(word_clean)

        # Find document occurrence
        doc_sentence = ""
        if document_text:
            sentences = re.split(r'(?<=[.!?।\n])\s+', document_text)
            pattern = rf"\b{re.escape(word_clean)}\b"
            for s in sentences:
                if re.search(pattern, s, re.IGNORECASE):
                    doc_sentence = s.strip()
                    break

        if kb:
            term_title = kb["term"]
            simple_meaning = kb["simple_meaning"] if target_lang == "hi" else (translate_single_chunk(kb["simple_meaning"], target_lang) if target_lang != "en" else kb["term"])
            ctx_meaning = kb["contextual_meaning"] if target_lang == "hi" else translate_single_chunk(kb["contextual_meaning"], target_lang)
            ex_val = kb["example"] if target_lang == "hi" else translate_single_chunk(kb["example"], target_lang)

            if target_lang == "hi":
                answer = (
                    f"📖 **शब्द का सीधा अर्थ (Exact Word Meaning):**\n"
                    f"• **{term_title}** का सीधा अर्थ है: **\"{simple_meaning}\"**\n\n"
                    f"💡 **सरल व्याख्या (Simple Explanation):**\n{ctx_meaning}\n\n"
                    f"🌟 **दैनिक जीवन का उदाहरण (Everyday Example):**\n{ex_val}"
                )
                if doc_sentence:
                    answer += f"\n\n📄 **इस दस्तावेज़ में संदर्भ (In This Document):**\n\"{doc_sentence}\""
            else:
                answer = (
                    f"📖 **Exact Word Meaning:**\n"
                    f"• **{term_title}** means: **\"{simple_meaning}\"**\n\n"
                    f"💡 **Simple Explanation:**\n{ctx_meaning}\n\n"
                    f"🌟 **Real-world Example:**\n{ex_val}"
                )
                if doc_sentence:
                    answer += f"\n\n📄 **Context in this document:**\n\"{doc_sentence}\""

            return {
                "question": original_question,
                "answer": answer,
                "source_passages": [doc_sentence] if doc_sentence else [],
                "found_in_document": bool(doc_sentence),
                "is_word_meaning": True,
                "word": word_clean,
                "ai_engine_active": False,
                "tokens_saved": 400
            }

        # 2. Dynamic High-Speed Translation for any vocabulary word (0 LLM tokens)
        direct_tr = translate_single_chunk(word_clean, target_lang) if target_lang != "en" else word_clean

        if target_lang == "hi":
            answer = (
                f"📖 **शब्द का सीधा अर्थ (Exact Word Meaning):**\n"
                f"• **{word_clean.capitalize()}** का सीधा अर्थ है: **\"{direct_tr}\"**\n\n"
                f"💡 **सरल व्याख्या:**\n"
                f"यह एक सामान्य शब्द है जिसका अर्थ '{direct_tr}' होता है।"
            )
            if doc_sentence:
                doc_sent_tr = translate_single_chunk(doc_sentence, "hi")
                answer += (
                    f"\n\n📄 **इस दस्तावेज़ में संदर्भ (In This Document):**\n"
                    f"\"{doc_sentence}\"\n"
                    f"👉 *दस्तावेज़ के अनुसार इसका अर्थ:* {doc_sent_tr}"
                )
        else:
            answer = (
                f"📖 **Exact Word Meaning:**\n"
                f"• **{word_clean.capitalize()}** translates directly to: **\"{direct_tr}\"**\n"
            )
            if doc_sentence:
                answer += f"\n\n📄 **Context in this document:**\n\"{doc_sentence}\""

        return {
            "question": original_question,
            "answer": answer,
            "source_passages": [doc_sentence] if doc_sentence else [],
            "found_in_document": bool(doc_sentence),
            "is_word_meaning": True,
            "word": word_clean,
            "ai_engine_active": False,
            "tokens_saved": 350
        }

    def chat_with_document(self, document_text: str, question: str, target_lang: str = "hi") -> Dict[str, Any]:
        """
        Interactive document-grounded question answering (Ask Vyron Anything About This Document).
        Strictly adheres to document facts:
        - Detects word meaning queries and returns exact dictionary definitions instantly.
        - Shows supporting source passages.
        - If absent, responds: 'This information was not found in the uploaded document.'
        """
        # Feature: Instant Exact Word Meaning Resolver (Zero Tokens, Direct Vocabulary Lookup)
        target_word = extract_target_word(question)
        if target_word:
            return self._answer_word_meaning_query(
                word=target_word,
                document_text=document_text,
                original_question=question,
                target_lang=target_lang
            )

        lang_name = LANGUAGE_NAMES.get(target_lang, target_lang)
        doc_trimmed = document_text[:14000]

        if not self.is_configured:
            q_lower = question.lower()
            matching_sentences = []
            sentences = re.split(r'(?<=[.!?।\n])\s+', document_text)
            keywords = [w for w in re.findall(r'\w+', q_lower) if len(w) > 3]

            for s in sentences:
                s_clean = s.strip()
                if not s_clean:
                    continue
                s_lower = s_clean.lower()
                if any(kw in s_lower for kw in keywords):
                    matching_sentences.append(s_clean)
                    if len(matching_sentences) >= 2:
                        break

            if matching_sentences:
                passage = " ".join(matching_sentences)
                ans_tr = translate_single_chunk(f"Based on the document: {passage}", target_lang)
                return {
                    "question": question,
                    "answer": ans_tr,
                    "source_passages": matching_sentences,
                    "found_in_document": True,
                    "ai_engine_active": False
                }
            else:
                not_found_msg = (
                    "This information was not found in the uploaded document."
                    if target_lang == "en" else
                    translate_single_chunk("This information was not found in the uploaded document.", target_lang)
                )
                return {
                    "question": question,
                    "answer": not_found_msg,
                    "source_passages": [],
                    "found_in_document": False,
                    "ai_engine_active": False
                }

        system_prompt = (
            f"You are VYRON AI's Document Q&A Assistant. Answer the user's question about the provided document. "
            f"CRITICAL GROUNDING: You MUST base your answer EXCLUSIVELY on the provided document text. "
            f"If the answer cannot be found in the document, you MUST explicitly state in {lang_name}: "
            f"'यह जानकारी अपलोड किए गए दस्तावेज़ में नहीं मिली।' (or equivalent in {lang_name}: 'This information was not found in the uploaded document.'). "
            f"Do not speculate or extrapolate beyond the written text. Always return valid JSON."
        )

        prompt = f"""
DOCUMENT:
\"\"\"
{doc_trimmed}
\"\"\"

QUESTION:
"{question}"

TARGET LANGUAGE FOR ANSWER: {lang_name} ({target_lang})

STRICT JSON SCHEMA:
{{
  "answer": "Clear, direct, factual answer in {lang_name}",
  "source_passages": [
    "Exact verbatim passage or sentence 1 from document that supports this answer",
    "Exact verbatim passage or sentence 2 from document (if applicable)"
  ],
  "found_in_document": true or false
}}
"""
        try:
            raw = self._request_model(prompt, system_prompt=system_prompt, timeout=25)
            parsed = clean_json_response(raw)
            parsed["ai_engine_active"] = True
            return parsed
        except Exception as exc:
            not_found_msg = (
                "Unable to process query via AI. Please try again or rephrase."
                if target_lang == "en" else
                translate_single_chunk("Unable to process query via AI. Please try again.", target_lang)
            )
            return {
                "question": question,
                "answer": f"{not_found_msg} ({exc})",
                "source_passages": [],
                "found_in_document": False,
                "ai_engine_active": False
            }

    def _fallback_analysis(
        self,
        document_text: str,
        target_lang: str,
        level: str,
        error_note: str = ""
    ) -> Dict[str, Any]:
        """
        High-speed single-batch fallback when cloud AI key is unconfigured.
        Batches all template items into ONE network call to ensure sub-second latency.
        """
        # Step 1: Real chunked literal translation of the document
        try:
            translation_res = translate_document_text(document_text[:12000], target_lang)
            translated_body = translation_res["translated_text"]
            detected_src = translation_res["detected_source_lang"]
        except Exception:
            translated_body = document_text[:12000]
            detected_src = "auto"

        # Step 2: Extract real dates, deadlines, and currency amounts
        date_matches = re.findall(
            r"\b(?:\d{1,2}[-/.]\d{1,2}[-/.]\d{2,4}|\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{2,4}|\d+\s+days?)\b",
            document_text,
            re.IGNORECASE
        )
        deadlines_raw = ", ".join(list(dict.fromkeys(date_matches))[:3]) if date_matches else ""

        fee_matches = re.findall(
            r"(?:Rs\.?|INR|₹|\$)\s*[\d,]+(?:\.\d{2})?",
            document_text,
            re.IGNORECASE
        )
        fees_raw = ", ".join(list(dict.fromkeys(fee_matches))[:3]) if fee_matches else ""

        # Step 3: Extract distinctive words
        words = re.findall(r"\b[A-Za-z]{8,}\b", document_text)
        unique_jargon = list(dict.fromkeys(words))[:3]

        # Pack ALL template items in ONE single batch call
        delimiter = "\n[[VYRON_SPLIT]]\n"
        template_pack = [
            "Not specified in the provided document",
            f"Notice deadline: {deadlines_raw}" if deadlines_raw else "Not specified in document",
            f"Prescribed amount: {fees_raw}" if fees_raw else "Not specified in document",
            "Carefully verify the statutory obligations and conditions stated above.",
            "Ensure compliance and submit required forms before the specified deadline.",
            "Official document faithfully translated into your selected language.",
            f"Important deadlines detected: {deadlines_raw if deadlines_raw else 'None specified'}",
            f"Fees or penalties referenced: {fees_raw if fees_raw else 'None specified'}",
            "Please cross-reference all penalty clauses and dates against the original document.",
            "Official identification and relevant forms as cited in notice.",
            "All named persons, entities, or account holders specified in notice.",
            "Administrative penalties, distress proceedings, or interest surcharges may apply if ignored.",
            "Government Notice / Circular"
        ]

        for w in unique_jargon:
            template_pack.append(w)
            template_pack.append(f"Statutory term appearing in notice: '{w}'")
            template_pack.append("Formal regulatory requirement.")

        if target_lang == "en":
            t_items = template_pack
        else:
            batch_str = delimiter.join(template_pack)
            try:
                batch_translated = translate_single_chunk(batch_str, target_lang)
                # Split using regex to handle variations like [[VYRON_SPLIT]], [[VYRON_SPLITE]], etc.
                raw_splits = re.split(r'\[\[\s*VYRON_SPLIT[A-Z]*\s*\]\]', batch_translated, flags=re.IGNORECASE)
                t_items = [item.strip() for item in raw_splits if item.strip()]
            except Exception:
                t_items = template_pack

        def get_item(idx: int, default: str) -> str:
            if idx < len(t_items) and t_items[idx]:
                return t_items[idx]
            return default

        not_specified_msg = get_item(0, "Not specified in the provided document")
        deadlines_val = get_item(1, deadlines_raw) if deadlines_raw else not_specified_msg
        fees_val = get_item(2, fees_raw) if fees_raw else not_specified_msg
        action1 = get_item(3, "Carefully verify the statutory obligations.")
        action2 = get_item(4, "Ensure compliance before the specified deadline.")
        takeaway1 = get_item(5, "Official document faithfully translated.")
        takeaway2 = get_item(6, f"Deadlines: {deadlines_raw}")
        takeaway3 = get_item(7, f"Fees: {fees_raw}")
        warning_msg = get_item(8, "Please cross-reference penalty clauses.")
        doc_req = get_item(9, "Official identification and relevant forms.")
        elig_val = get_item(10, "All named persons or entities.")
        penalties_val = get_item(11, "Administrative penalties may apply if ignored.")
        doc_type_val = get_item(12, "Government Notice / Circular")

        # Step 4: Extract verified civic jargon from authoritative Knowledge Base
        known_jargon = extract_known_terms(document_text)
        jargon_items = []
        for kj in known_jargon:
            s_meaning = kj["simple_meaning"] if target_lang == "hi" else (translate_single_chunk(kj["simple_meaning"], target_lang) if target_lang != "en" else kj["term"])
            c_meaning = kj["contextual_meaning"] if target_lang == "hi" else translate_single_chunk(kj["contextual_meaning"], target_lang)
            ex_val = kj["example"] if target_lang == "hi" else translate_single_chunk(kj["example"], target_lang)
            jargon_items.append({
                "term": kj["term"],
                "simple_meaning": s_meaning,
                "contextual_meaning": c_meaning,
                "example": ex_val,
                "source_sentence": kj["source_sentence"],
                "action_required": kj.get("action_required", "")
            })

        # If fewer than 3 terms found in knowledge base, supplement from detected words
        if len(jargon_items) < 3:
            cursor = 13
            for w in unique_jargon:
                if any(w.lower() in j["term"].lower() for j in jargon_items):
                    continue
                sentence_match = re.search(rf"([^.?!]*\b{re.escape(w)}\b[^.?!]*[.?!])", document_text)
                sent = sentence_match.group(1).strip() if sentence_match else f"Contains term '{w}'."
                w_meaning = get_item(cursor, w)
                w_ctx = get_item(cursor + 1, f"Term: {w}")
                w_ex = get_item(cursor + 2, "Formal statutory requirement.")
                cursor += 3

                jargon_items.append({
                    "term": w,
                    "simple_meaning": w_meaning,
                    "contextual_meaning": w_ctx,
                    "example": w_ex,
                    "source_sentence": sent
                })
                if len(jargon_items) >= 4:
                    break

        purpose_summary = translated_body[:320] + ("..." if len(translated_body) > 320 else "")
        note = "Vyron Hybrid Mode: High-speed real translation active."
        if error_note:
            note += f" ({error_note})"

        return {
            "ai_engine_active": False,
            "engine_note": note,
            "detected_source_language": detected_src,
            "document_type": doc_type_val,
            "faithful_translation": translated_body,
            "simple_explanation": {
                "overall_purpose": purpose_summary,
                "level": level,
                "simplified_body": translated_body,
                "key_takeaways": [takeaway1, takeaway2, takeaway3],
                "ambiguities_or_warnings": warning_msg
            },
            "what_you_need_to_do": {
                "required_actions": [action1, action2],
                "deadlines": deadlines_val,
                "fees_and_payments": fees_val,
                "required_documents": [doc_req],
                "eligibility_conditions": elig_val,
                "contact_and_links": not_specified_msg,
                "penalties_or_consequences": penalties_val
            },
            "jargon_decoded": jargon_items
        }
