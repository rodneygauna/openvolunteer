"""Forms for the messages feature of the application."""
# Imports
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired


# Form - Send Message
class SendMessage(FlaskForm):
    """Send a message form"""
    message_to_id = SelectField("To", coerce=int, validators=[DataRequired()])
    message = TextAreaField("Message", validators=[DataRequired()])
    submit = SubmitField("Send")
