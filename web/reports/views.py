"""View for the reports portion of the application."""
# Imports
import io
import csv
from datetime import datetime
from flask import Blueprint, request, render_template, make_response
from flask_login import login_required, current_user
from .forms import GenerateReportForm
from .queries import (
    waiver_signees,
)
from waivers.models import Waiver


# Blueprint Configuration
reports_bp = Blueprint("reports", __name__)


# Reports
@reports_bp.route("/reports", methods=["GET", "POST"])
@login_required
def generate_report():
    """Route for generating and viewing reports."""

    form = GenerateReportForm()

    # Report Options
    # Make sure to update the following functions:
    # - get_column_labels()
    # - generate_report_data()
    form.report_options.choices = [
        ("Waiver Signees", "Waiver Signees"),
    ]
    form.waiver_id.choices = [
        (w.id, w.version) for w in Waiver.query.order_by(Waiver.id.desc()).all()]

    if request.method == "POST":
        # Get the selected report and date parameters from the form
        selected_report = form.report_options.data
        params = {
            "start_date": form.start_date.data if form.start_date.data else "",
            "end_date": form.end_date.data if form.end_date.data else "",
            "waiver_id": form.waiver_id.data if form.waiver_id.data else "",
        }

        # Generate report data based on the selected report and date parameters
        report_data = generate_report_data(
            selected_report, params)

        # Define custom column labels based on the selected report
        column_labels = get_column_labels(selected_report)
        # Count of the columns for the selected report
        column_count = len(column_labels)

        # Render the report template with the generated data
        return render_template(
            "reports/report.html",
            title="OpenVolunteer - Report",
            report_data=report_data,
            selected_report=selected_report,
            params=params,
            column_labels=column_labels,
            column_count=column_count,
        )

    return render_template(
        "reports/generate_report.html",
        title="OpenVolunteer - Generate Report",
        form=form,
    )


def generate_report_data(report, params):
    """
    Generate report data based on the selected report
    and date parameters.
    """

    # Waiver Signees Report
    if report == "Waiver Signees":
        waiver_id = params.get("waiver_id")
        if waiver_id is None:
            raise ValueError("Missing required parametere 'waiver_id'")
        return waiver_signees(waiver_id)
    else:
        # Handle other report options if needed
        return []


def get_column_labels(report):
    """Get custom column labels based on the selected report."""

    # Waiver Signee - Column Labels
    if report == "Waiver Signees":
        return [
            "Waiver ID",
            "Signee Agreement Date",
            "Signee First Name",
            "Signee Last Name",
            "Signee Date of Birth",
            "Signee User ID",
            "User ID",
            "User First Name",
            "User Last Name",
        ]
    else:
        # Handle other report options if needed
        return []


# Generate CSV Report
@reports_bp.route("/reports/export-csv", methods=["POST"])
@login_required
def export_csv():
    """Route for exporting report data as CSV."""

    # Current Time
    current_time = datetime.utcnow()

    # Get all form data as a dictionary
    form_data = request.form.to_dict()

    # Get the selected report from the form data
    selected_report = form_data.pop("selected_report")

    # Generate report data based on the selected report and parameters
    report_data = generate_report_data(selected_report, form_data)

    # Define custom column labels based on the selected report
    column_labels = get_column_labels(selected_report)

    # Generate a CSV file in memory
    csv_output = generate_csv(report_data, column_labels)

    # Create a response with the CSV file
    response = make_response(csv_output.getvalue())

    # Set the appropriate headers for CSV download
    response.headers[
        "Content-Disposition"
    ] = f"attachment; filename={selected_report}_{current_time}.csv"
    response.headers["Content-type"] = "text/csv"

    return response


def generate_csv(data, column_labels):
    """Generate a CSV file from the provided data and column labels."""
    output = io.StringIO()
    writer = csv.writer(output)

    # Write the header row
    writer.writerow(column_labels)

    # Write the data rows
    for row in data:
        writer.writerow(row)

    return output
