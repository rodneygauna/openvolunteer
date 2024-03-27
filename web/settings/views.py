"""Views for the settings portion of the application."""
# Imports
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from users.admin_superuser import admin_required, superuser_required
from app import db
from .queries import get_users
from .forms import OrganizationForm, DefaultPreferenceForm, LocationForm
from .models import Organization, DefaultPreference, Location


# Blueprint
settings_bp = Blueprint("settings", __name__, url_prefix="/settings")


# Route - View Organization
@settings_bp.route("/organization", methods=["GET"])
@login_required
@admin_required
def view_organization():
    """View organization details."""
    organization = Organization.query.first()
    return render_template("settings/organization.html",
                           organization=organization)


# Route - Create/Edit Organization

@settings_bp.route("/organization/create", methods=["GET", "POST"])
@login_required
@admin_required
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
@settings_bp.route("/default-preferences", methods=["GET"])
@login_required
@admin_required
def view_default_preferences():
    """View default preferences."""
    default_preferences = DefaultPreference.query.first()
    return render_template("settings/default_preferences.html",
                           default_preferences=default_preferences)


# Route - Create/Edit Default Preferences
@settings_bp.route("/default-preferences/create", methods=["GET", "POST"])
@login_required
@admin_required
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
@settings_bp.route("/locations", methods=["GET"])
@login_required
@superuser_required
def view_locations():
    """View locations."""
    locations = Location.query.all()
    return render_template("settings/locations.html", locations=locations)


# Route - Create Locations
@settings_bp.route("/locations/create", methods=["GET", "POST"])
@login_required
@superuser_required
def create_location():
    """Create locations."""
    form = LocationForm()
    if form.validate_on_submit():
        location = Location()
        form.populate_obj(location)
        location.created_by = current_user.id
        db.session.add(location)
        db.session.commit()
        return redirect(url_for("settings.view_locations"))
    return render_template("settings/location_form.html", form=form)


# Route - Edit Locations
@settings_bp.route("/locations/edit/<int:location_id>",
                   methods=["GET", "POST"])
@login_required
@superuser_required
def edit_location(location_id):
    """Edit locations."""
    location = Location.query.get_or_404(location_id)
    form = LocationForm(obj=location)
    if form.validate_on_submit():
        form.populate_obj(location)
        location.updated_date = datetime.utcnow()
        location.updated_by = current_user.id
        db.session.commit()
        return redirect(url_for("settings.view_locations"))
    return render_template("settings/location_form.html", form=form)


# Route - User Management
@settings_bp.route("/users", methods=["GET"])
@login_required
@admin_required
def view_users():
    """View all users."""
    users = get_users()
    return render_template("settings/users.html", users=users)
