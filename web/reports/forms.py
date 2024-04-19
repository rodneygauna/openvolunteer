"""Report forms for the reports blueprint."""
# Imports
from datetime import datetime, timedelta
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, DateField
from wtforms.validators import DataRequired


# Form - Generate Report
class GenerateReportForm(FlaskForm):
    """Select and generate a report"""

    start_date = datetime.now() - timedelta(days=30)

    report_options = SelectField(
        label="Report *",
        coerce=str,
        validators=[DataRequired()],
    )
    start_date = DateField(
        label="Start Date",
        format="%Y-%m-%d",
        default=start_date
    )
    end_date = DateField(
        label="End Date",
        format="%Y-%m-%d",
        default=datetime.now()
    )
    waiver_id = SelectField(
        label="Waiver",
        coerce=int,
    )
    submit = SubmitField(label="Generate Report")
