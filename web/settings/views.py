"""Views for the settings portion of the application."""
# Imports
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from users.admin_superuser import admin_required, superuser_required
from app import db
from .forms import OrganizationForm, DefaultPreferenceForm, LocationForm
from .models import Organization, DefaultPreference, Location


# Blueprint
settings_bp = Blueprint("settings", __name__, url_prefix="/settings")


# Route - View Organization
@login_required
@admin_required
@settings_bp.route("/organization", methods=["GET"])
def view_organization():
    """View organization details."""
    organization = Organization.query.first()
    return render_template("settings/organization.html",
                           organization=organization)


# Route - Create/Edit Organization
@login_required
@admin_required
@settings_bp.route("/organization/create", methods=["GET", "POST"])
def create_organization():
    """Create or edit organization details."""
    organization = Organization.query.first()
    form = OrganizationForm(obj=organization)
    if form.validate_on_submit():
        if organization:
            form.populate_obj(organization)
        else:
            organization = Organization()
            form.populate_obj(organization)
            organization.created_by = current_user.id
            organization.updated_date = datetime.utcnow()
            organization.updated_by = current_user.id
            db.session.add(organization)
        db.session.commit()
        return redirect(url_for("settings.view_organization"))
    return render_template("settings/organization_form.html", form=form)


# Route - View Default Preferences
@login_required
@admin_required
@settings_bp.route("/default-preferences", methods=["GET"])
def view_default_preferences():
    """View default preferences."""
    default_preferences = DefaultPreference.query.first()
    return render_template("settings/default_preferences.html",
                           default_preferences=default_preferences)


# Route - Create/Edit Default Preferences
@login_required
@admin_required
@settings_bp.route("/default-preferences/create", methods=["GET", "POST"])
def create_default_preferences():
    """Create or edit default preferences."""
    default_preferences = DefaultPreference.query.first()
    form = DefaultPreferenceForm(obj=default_preferences)
    if form.validate_on_submit():
        if default_preferences:
            form.populate_obj(default_preferences)
        else:
            default_preferences = DefaultPreference()
            form.populate_obj(default_preferences)
            default_preferences.created_by = current_user.id
            default_preferences.updated_date = datetime.utcnow()
            default_preferences.updated_by = current_user.id
            db.session.add(default_preferences)
        db.session.commit()
        return redirect(url_for("settings.view_default_preferences"))
    return render_template("settings/default_preferences_form.html", form=form)


# Route - View Locations
@login_required
@superuser_required
@settings_bp.route("/locations", methods=["GET"])
def view_locations():
    """View locations."""
    locations = Location.query.all()
    return render_template("settings/locations.html", locations=locations)


# Route - Create/Edit Locations
@login_required
@superuser_required
@settings_bp.route("/locations/create", methods=["GET", "POST"])
def create_location():
    """Create or edit locations."""
    location = Location.query.first()
    form = LocationForm(obj=location)
    if form.validate_on_submit():
        if location:
            form.populate_obj(location)
        else:
            location = Location()
            form.populate_obj(location)
            location.created_by = current_user.id
            location.updated_date = datetime.utcnow()
            location.updated_by = current_user.id
            db.session.add(location)
        db.session.commit()
        return redirect(url_for("settings.view_locations"))
    return render_template("settings/location_form.html", form=form)
