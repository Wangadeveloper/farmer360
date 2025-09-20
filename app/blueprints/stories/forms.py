from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class CommentForm(FlaskForm):
    username = StringField("Your Name", validators=[DataRequired()])
    comment = TextAreaField("Comment", validators=[DataRequired()])
    submit = SubmitField("Post Comment")
