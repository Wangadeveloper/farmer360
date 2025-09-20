from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired

class FinanceAdviceForm(FlaskForm):
    farm_type = SelectField("Farm Type", choices=[("crop", "Crop Farming"), ("livestock", "Livestock Farming")], validators=[DataRequired()])
    product = StringField("Product (e.g., maize, milk)", validators=[DataRequired()])
    target_market = StringField("Target Market (local, export, etc.)", validators=[DataRequired()])
    submit = SubmitField("Get Advice")
