from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired

class ChemicalInquiryForm(FlaskForm):
    image = FileField("Upload Chemical Image (bonyeza ili kuweka picha ya kemikali)", validators=[DataRequired()])
    submit = SubmitField("Analyze (pata ushauri)")
