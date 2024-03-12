"""Notification forms for the application."""
# Imports
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired


# Form - Notification
class NotificationForm(FlaskForm):
    """Notification form"""

    title = StringField("Title", validators=[DataRequired()])
    message = TextAreaField("Message", validators=[DataRequired()])
    status = SelectField("Status", choices=[
                         ("active", "Active"), ("inactive", "Inactive")])
    submit = SubmitField("Save Notification")
