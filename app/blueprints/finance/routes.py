import re
from flask import render_template, request, flash, make_response
from . import finance_bp
from .forms import FinanceAdviceForm
from app.utils.ai_helpers import get_model, generate_pdf
from app.utils.translation import translate_to_swahili


@finance_bp.route("/finance", methods=["GET", "POST"])
def finance():
    form = FinanceAdviceForm()

    if form.validate_on_submit():
        # Build query
        query = f"""
        Advise a farmer in {form.farm_type.data} who produces {form.product.data}
        and wants to sell in {form.target_market.data}.
        Provide market entry, revenue growth, investments, risks and solutions.
        """

        # ✅ Use Gemini model directly to get English text
        model = get_model("gemini-1.5-flash")
        eng_text = model.generate_content(query).text

        # ✅ Translate English advice to Swahili
        sw_text = translate_to_swahili(eng_text)

        # ✅ Merge both advices into one PDF
        combined_text = f"""
        📊 Financial Advice Report

        --- English Version ---
        {eng_text}

        --- Swahili Version ---
        {sw_text}
        """
        pdf_output = generate_pdf(combined_text, title="Financial Advice Report")

        # ✅ Stream PDF to browser
        response = make_response(pdf_output.read())
        response.headers["Content-Type"] = "application/pdf"
        response.headers["Content-Disposition"] = 'inline; filename="financial_advice.pdf"'
        return response

    return render_template("finance/finance.html", form=form)
