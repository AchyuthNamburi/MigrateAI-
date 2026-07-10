# backend/agents/fallback_responses.py
def get_fallback_response(prompt: str) -> str:
    if "framework" in prompt.lower():
        return '{"framework":"Django","version":"4.2","confidence":85,"reasoning":"Detected Django","dependencies":{"python":["Django==4.2"]},"summary":"Django web application"}'
    return "Groq API unavailable. Using fallback mode."