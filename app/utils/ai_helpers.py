import os
from io import BytesIO
from PIL import Image
import google.generativeai as genai
from fpdf import FPDF
from flask import current_app

def generate_pdf(content: str, title: str = "AI Advice") -> BytesIO:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", style="B", size=16)
    pdf.cell(0, 10, title, ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", size=12)
    # Strip or replace emojis (non-ASCII chars)
    cleaned_content = content.encode("ascii", "ignore").decode()
    pdf.multi_cell(0, 8, cleaned_content)

    pdf_output = BytesIO()
    pdf_output.write(pdf.output(dest="S").encode("latin1", errors="replace"))
    pdf_output.seek(0)
    return pdf_output



# ✅ Configure Gemini safely inside request context
def get_model(model_name="gemini-1.5-flash"):
    # Get API key from Flask config or fallback to environment variable
    api_key = current_app.config.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise RuntimeError("❌ GOOGLE_API_KEY is not set in environment variables or config")

    genai.configure(api_key=api_key)

    generation_config = {
        "temperature": 0.3,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    return genai.GenerativeModel(model_name=model_name, generation_config=generation_config)


# 🔹 Disease Analysis
def get_disease_analysis(farm_type: str, image_path: str) -> BytesIO:
    try:
        img = Image.open(image_path)
        prompt = f"""
        You are a veterinary and crop health assistant.
        The farmer has a **{farm_type}**.

        Analyze the uploaded image for signs of disease, pests, or malnutrition.
        Provide:
        1. Diagnosis (what could be wrong with the {farm_type})
        2. Actionable steps
        3. When to consult a vet/agronomist
        """
        model = get_model("gemini-1.5-flash")  # ✅ supports text + image
        response = model.generate_content([prompt, img])
        return generate_pdf(response.text, title=f"Disease Analysis Report ({farm_type.capitalize()})")
    except Exception as e:
        return generate_pdf(f"Error analyzing {farm_type}: {str(e)}", title="Error Report")


# 🔹 Financial Advice
def get_financial_advice(farm_data: str) -> BytesIO:
    try:
        prompt = f"""
        You are an agricultural financial advisor.
        Given this farm situation:
        {farm_data}

        Provide simple, clear advice on:
        - Revenue optimization
        - Investment opportunities
        - Risk management
        """
        model = get_model("gemini-1.5-flash")  # ✅ text-only works too
        response = model.generate_content(prompt)
        return generate_pdf(response.text, title="Financial Advice Report")
    except Exception as e:
        return generate_pdf(f"Error generating financial advice: {str(e)}", title="Error Report")


# 🔹 Chemical Advice (return TEXT, not PDF)
def get_chemical_advice(image_path: str) -> str:
    try:
        img = Image.open(image_path)
        prompt = """
        You are an agricultural safety expert.
        Analyze this farm chemical image/label.
        Provide:
        1. Chemical name and purpose
        2. Safe usage instructions
        3. Health/environmental risks
        4. Eco-friendly alternatives if possible
        """
        model = get_model("gemini-1.5-flash")  # vision-capable model
        response = model.generate_content([prompt, img])
        return response.text.strip()
    except Exception as e:
        return f"Error analyzing chemical: {str(e)}"


# 🔹 Translation
def translate_advice(advice: str, target_lang: str = "sw") -> BytesIO:
    try:
        prompt = f"""
        Translate the following farming advisory into {target_lang}.
        Keep the meaning clear and simple for farmers.

        Text:
        {advice}
        """
        model = get_model("gemini-1.5-flash")  # ✅ best for translations too
        response = model.generate_content(prompt)
        return generate_pdf(response.text, title=f"Advice in {target_lang.upper()}")
    except Exception as e:
        return generate_pdf(f"Error translating advice: {str(e)}", title="Error Report")
