from flask_wtf import FlaskForm
from wtforms import SelectField, FileField, SubmitField
from wtforms.validators import DataRequired

class DiseaseCheckForm(FlaskForm):
    farm_type = SelectField(
        "Farm Type",
        choices=[("crop", "Crop (MMea)"), ("livestock", "Livestock (Mnyama)")],
        validators=[DataRequired()]
    )
    image = FileField("Upload Image (bonyeza ili kuweka picha)", validators=[DataRequired()])
    submit = SubmitField("Analyze (pata uhauri)")

