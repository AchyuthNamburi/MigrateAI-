# backend/core/llm.py
from langchain_groq import ChatGroq
from backend.config import settings
import logging

logger = logging.getLogger(__name__)

def get_llm():
    try:
        if settings.GROQ_API_KEY and settings.GROQ_API_KEY != "dummy":
            return ChatGroq(
                api_key=settings.GROQ_API_KEY,
                model="llama-3.1-8b-instant",
                temperature=0.1,
                max_tokens=2048
            )
    except Exception as e:
        logger.warning(f"Groq unavailable: {e}")
    
    logger.info("Using fallback LLM")
    from backend.agents.fallback_responses import get_fallback_response
    return FallbackLLM()

class FallbackLLM:
    def invoke(self, prompt: str):
        from backend.agents.fallback_responses import get_fallback_response
        return get_fallback_response(prompt)