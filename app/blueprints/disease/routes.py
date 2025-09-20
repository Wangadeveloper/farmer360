import os
import re
from flask import render_template, request, current_app, flash, make_response
from werkzeug.utils import secure_filename
from flask_login import login_required
from . import disease_bp
from .forms import DiseaseCheckForm
from app.utils.ai_helpers import get_model, generate_pdf
from app.utils.translation import translate_to_swahili
from PIL import Image


@disease_bp.route("/disease-check", methods=["GET", "POST"])
# @login_required
def disease_check():
    form = DiseaseCheckForm()

    if form.validate_on_submit():
        # Save uploaded file
        file = form.image.data
        filename = secure_filename(file.filename)
        save_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
        file.save(save_path)

        # 🔹 Step 1: Get English advice (TEXT not PDF yet)
        model = get_model("gemini-1.5-flash")
        img = Image.open(save_path)
        prompt = f"""
        You are a veterinary and crop health assistant.
        The farmer has a **{form.farm_type.data}**.

        Analyze the uploaded image for signs of disease, pests, or malnutrition.
        Provide:
        1. Diagnosis (what could be wrong with the {form.farm_type.data})
        2. Actionable steps
        3. When to consult a vet/agronomist
        """
        eng_response = model.generate_content([prompt, img])
        english_advice = eng_response.text

        # 🔹 Step 2: Translate to Swahili
        swahili_advice = translate_to_swahili(english_advice)

        # 🔹 Step 3: Combine into one PDF
        combined_content = (
            "🐄 Disease Analysis Report\n\n"
            "=== English Advice ===\n\n"
            f"{english_advice}\n\n"
            "=== Ushauri kwa Kiswahili ===\n\n"
            f"{swahili_advice}"
        )
        pdf_output = generate_pdf(combined_content, title="Disease Analysis Report")

        # 🔹 Step 4: Stream PDF response
        response = make_response(pdf_output.read())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'inline; filename="disease_analysis_{form.farm_type.data}.pdf"'
        return response

    return render_template("disease/disease_check.html", form=form)
