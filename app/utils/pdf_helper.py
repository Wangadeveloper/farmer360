from fpdf import FPDF
from io import BytesIO

def generate_pdf(content: str, title: str = "AI Advice") -> BytesIO:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)

    # Add a title
    pdf.set_font("Arial", style="B", size=16)
    pdf.cell(0, 10, title, ln=True, align="C")
    pdf.ln(10)

    # Reset font
    pdf.set_font("Arial", size=12)

    # Clean content and add
    cleaned_content = content.replace("\u2013", "-")
    pdf.multi_cell(0, 8, cleaned_content)

    # Save to memory
    pdf_output = BytesIO()
    pdf_output.write(pdf.output(dest="S").encode("latin1", errors="replace"))
    pdf_output.seek(0)
    return pdf_output
