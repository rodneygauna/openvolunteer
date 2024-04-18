"""Waiver forms for the waivers feature of the application."""
# Imports
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


# Form - Waiver
class WaiverForm(FlaskForm):
    """Waiver form"""
    current_date = datetime.now().strftime("%Y-%m-%d")

    active_date = DateField("Active Date",
                            format="%Y-%m-%d",
                            validators=[DataRequired()])
    expiration_date = DateField("Expiration Date",
                                format="%Y-%m-%d")
    version = StringField("Version",
                          default=str(current_date),
                          validators=[DataRequired()])
    content = TextAreaField("Content (HTML)",
                            render_kw={"rows": 20},
                            validators=[DataRequired()])
    signature_consent = TextAreaField("Content (HTML)",
                                      render_kw={"rows": 10},
                                      validators=[DataRequired()])
    submit = SubmitField("Save")
    cancel = SubmitField('Cancel', render_kw={'formnovalidate': True})


# Form - Waiver Agreement
class WaiverAgreementForm(FlaskForm):
    """Waiver agreement form"""
    signee_first_name = StringField("First Name",
                                    validators=[DataRequired()])
    signee_last_name = StringField("Last Name",
                                   validators=[DataRequired()])
    signee_date_of_birth = DateField("Date of Birth",
                                     format="%Y-%m-%d",
                                     validators=[DataRequired()])
    submit = SubmitField("I Agree")
    cancel = SubmitField('Cancel', render_kw={'formnovalidate': True})
