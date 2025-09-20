from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class FarmRecordForm(FlaskForm):
    farm_type = SelectField("Farm Type", choices=[("crop", "Crop"), ("livestock", "Livestock")], validators=[DataRequired()])
    name = StringField("Name of Crop/Animal", validators=[DataRequired()])
    quantity = IntegerField("Quantity (e.g., acres or number of animals)", validators=[DataRequired()])
    notes = TextAreaField("Additional Notes")
    submit = SubmitField("Save Record")
