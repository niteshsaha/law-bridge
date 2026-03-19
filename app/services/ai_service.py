import os
from dotenv import load_dotenv
import requests
import logging
from google import genai
import streamlit as st

# ==============================
# 🔹 LOAD ENV + LOGGING
# ==============================
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 🔥 Safe import (avoid crash)
try:
    import streamlit as st
    API_KEY = st.secrets.get("API_KEY")
    AI_PROVIDER = st.secrets.get("AI_PROVIDER", "ollama")
except Exception:
    API_KEY = None
    AI_PROVIDER = None

# 🔥 Fallback to .env
if not API_KEY:
    API_KEY = os.getenv("API_KEY")

if not AI_PROVIDER:
    AI_PROVIDER = os.getenv("AI_PROVIDER", "ollama")

logger.info(f"[AI] Provider: {AI_PROVIDER}")

# ==============================
# 🔹 GEMINI SETUP (NEW SDK)
# ==============================
if AI_PROVIDER == "gemini":
    client = genai.Client(api_key=API_KEY)
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3-flash-preview")


# ==============================
# 🔹 MAIN ENTRY
# ==============================
def generate_explanation(source_text, target_text, diff):
    logger.info(f"[AI] Using provider: {AI_PROVIDER}")

    if AI_PROVIDER == "gemini":
        return generate_with_gemini(source_text, target_text, diff)
    else:
        return generate_with_ollama(source_text, target_text, diff)


# ==============================
# 🔹 GEMINI IMPLEMENTATION
# ==============================
def generate_with_gemini(source_text, target_text, diff):
    try:
        text = target_text  # ✅ FIX

        if not text:
            return "No explanation available."

        logger.info("[AI] Calling Gemini API...")

        prompt = f"""
        Explain this law in very simple English.

        Focus:
        - What it means
        - Who it applies to
        - What happens if violated

        Law:
        {text[:400]}

        Rules:
        - Max 3 bullet points
        - No legal jargon
        - Keep it short
        """

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )

        text = response.text if response and response.text else None

        if text:
            logger.info("[AI] Gemini response received")
            return text.strip()
        else:
            logger.warning("[AI] Gemini empty response")
            return fallback_to_ollama(source_text, target_text, diff)

    except Exception as e:
        logger.error(f"[AI] Gemini error: {e}")
        return fallback_to_ollama(source_text, target_text, diff)


# ==============================
# 🔹 OLLAMA IMPLEMENTATION
# ==============================
def generate_with_ollama(source_text, target_text, diff):
    try:
        logger.info("[AI] Calling Ollama...")

        prompt = f"""
Explain the difference between two laws in simple English.

Old Law:
{source_text[:400]}

New Law:
{target_text[:400]}

Changes:
Added: {diff['added']}
Removed: {diff['removed']}
"""

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "qwen2.5:1.5b",
                "prompt": prompt,
                "stream": False
            },
            timeout=30
        )

        result = response.json().get("response", "").strip()

        logger.info("[AI] Ollama response received")

        return result if result else "Ollama returned empty response."

    except Exception as e:
        logger.error(f"[AI] Ollama error: {e}")
        return "AI service not available."


# ==============================
# 🔹 FALLBACK LOGIC
# ==============================
def fallback_to_ollama(source_text, target_text, diff):
    logger.warning("[AI] Falling back to Ollama...")
    return generate_with_ollama(source_text, target_text, diff)