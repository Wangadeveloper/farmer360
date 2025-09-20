import google.generativeai as genai1
from flask import current_app

def get_translator():
    """Initialize and return a Gemini translator instance using app config."""
    genai1.configure(api_key=current_app.config['GOOGLE_API_KEY1'])
    return genai1.GenerativeModel("gemini-1.5-flash")

def translate_to_swahili(text: str) -> str:
    """Translate English text to Swahili using Gemini."""
    translator = get_translator()   # ✅ now it's created inside the request context
    prompt = f"Translate this to Swahili:\n\n{text}"
    response = translator.generate_content(prompt)
    return response.text
