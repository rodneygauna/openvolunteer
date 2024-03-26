"""Setting forms for the application."""
# Imports
from flask_wtf import FlaskForm
from wtforms import (
    SubmitField, SelectField, TextAreaField,
    StringField)
from wtforms.validators import DataRequired
from events.dictionary import TIMEZONES


# Form - Create/Edit Organization
class OrganizationForm(FlaskForm):
    """Create/Edit organization form"""

    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email")
    phone = StringField("Phone")
    fax = StringField("Fax")
    address_1 = StringField("Address 1")
    address_2 = StringField("Address 2")
    city = StringField("City")
    state = StringField("State")
    postal_code = StringField("Postal Code")
    mailing_address_1 = StringField("Mailing Address 1")
    mailing_address_2 = StringField("Mailing Address 2")
    mailing_city = StringField("Mailing City")
    mailing_state = StringField("Mailing State")
    mailing_postal_code = StringField("Mailing Postal Code")
    submit = SubmitField("Save Organization")


# Form - Create/Edit Default Preferences
class DefaultPreferenceForm(FlaskForm):
    """Create/Edit default preference form"""

    default_timezone = SelectField("Default Timezone for Events",
                                   choices=TIMEZONES,
                                   validators=[DataRequired()])
    submit = SubmitField("Save Default Preferences")


# Form - Create/Edit Locations
class LocationForm(FlaskForm):
    """Create/Edit location form"""

    name = StringField("Name", validators=[DataRequired()])
    short_name = StringField("Short Name", validators=[DataRequired()])
    email = StringField("Email")
    phone = StringField("Phone")
    fax = StringField("Fax")
    address_1 = StringField("Address 1")
    address_2 = StringField("Address 2")
    city = StringField("City")
    state = StringField("State")
    postal_code = StringField("Postal Code")
    mailing_address_1 = StringField("Mailing Address 1")
    mailing_address_2 = StringField("Mailing Address 2")
    mailing_city = StringField("Mailing City")
    mailing_state = StringField("Mailing State")
    mailing_postal_code = StringField("Mailing Postal Code")
    comments = TextAreaField("Comments")
    submit = SubmitField("Save Location")
