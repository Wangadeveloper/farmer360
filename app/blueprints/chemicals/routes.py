import os
import re
from flask import render_template, request, current_app, flash, make_response
from werkzeug.utils import secure_filename
from . import chemicals_bp
from .forms import ChemicalInquiryForm
from app.utils.ai_helpers import get_chemical_advice, generate_pdf
from app.utils.translation import translate_to_swahili


@chemicals_bp.route("/chemicals", methods=["GET", "POST"])
def chemicals():
    form = ChemicalInquiryForm()

    if form.validate_on_submit():
        # Save uploaded file
        file = form.image.data
        filename = secure_filename(file.filename)
        save_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
        file.save(save_path)

        # Get AI advice (English TEXT)
        eng_advice = get_chemical_advice(save_path)

        # Translate to Swahili (TEXT)
        sw_advice = translate_to_swahili(eng_advice)

        # Combine into one PDF
        combined_content = (
            "Chemical Safety Report\n\n"
            "--- English Version ---\n"
            f"{eng_advice}\n\n"
            "--- Swahili Version ---\n"
            f"{sw_advice}"
        )

        pdf_output = generate_pdf(combined_content, title="Chemical Safety Report")

        # Stream PDF response
        response = make_response(pdf_output.read())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'inline; filename=chemical_safety_report.pdf'
        return response

    return render_template("chemicals/chemicals.html", form=form)
