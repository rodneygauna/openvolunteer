"""
Event forms for the application.
"""
# Imports
from flask_wtf import FlaskForm
from wtforms import (SubmitField, SelectField, TextAreaField,
                     DateField, TimeField)
from wtforms.validators import DataRequired
from .dictionary import (EVENT_STATUS, TIMEZONES)


# Form - Create Event
class EventForm(FlaskForm):
    """Create an event form"""

    start_date = DateField("Start Date", format='%Y-%m-%d',
                           validators=[DataRequired()])
    start_time = TimeField("Start Time", format='%H:%M',
                           validators=[DataRequired()])
    start_timezone = SelectField("Timezone", choices=TIMEZONES,
                                 default="UTC", validators=[DataRequired()])
    title = TextAreaField("Title", validators=[DataRequired()])
    description = TextAreaField("Description")
    max_attendees = SelectField("Max Attendees",
                                choices=[(i, i) for i in range(1, 21)],
                                default=10, coerce=int)
    event_status = SelectField("Event Status", choices=EVENT_STATUS)
    submit = SubmitField("Save Event")


# Form - Event Signup
class EventSignupForm(FlaskForm):
    """Event signup form"""

    comments = TextAreaField("Comments")
    submit = SubmitField("Sign Up")
