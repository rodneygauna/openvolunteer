"""Waiver views for the waivers feature of the application."""
# Imports
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from users.admin_superuser import admin_required
from .queries import get_waivers
from .forms import WaiverForm, WaiverAgreementForm
from .models import Waiver, WaiverAgreement


# Blueprint - Settings - Waivers
waiver_bp = Blueprint('waivers', __name__)


# Waiver - View All Waivers
@waiver_bp.route('settings/waivers', methods=['GET'])
@login_required
@admin_required
def view_waivers():
    """View all waivers"""
    waivers = get_waivers()
    return render_template('waivers/waivers.html', waivers=waivers)


# Waiver - Settings - View Waiver
@waiver_bp.route('settings/waivers/<int:waiver_id>',
                 methods=['GET'])
@login_required
@admin_required
def view_waiver(waiver_id):
    """View waiver details"""
    waiver = get_waivers(waiver_id)
    return render_template('waivers/waiver.html', waiver=waiver)


# Waiver - Settings - Create Waiver
@waiver_bp.route('settings/waivers/create',
                 methods=['GET', 'POST'])
@login_required
@admin_required
def create_waiver():
    """Create a waiver"""
    form = WaiverForm()
    if form.validate_on_submit():
        waiver = Waiver()
        form.populate_obj(waiver)
        waiver.created_by = current_user.id
        waiver.created_date = datetime.utcnow()
        db.session.add(waiver)
        db.session.commit()
        flash('Waiver created successfully.', 'success')
        return redirect(url_for('waivers.view_waiver'))
    return render_template('waivers/waiver_form.html', form=form)


# Waiver - Settings - Edit Waiver
@waiver_bp.route('settings/waivers/edit/<int:waiver_id>',
                 methods=['GET', 'POST'])
@login_required
@admin_required
def edit_waiver(waiver_id):
    """Edit waiver details"""
    waiver = Waiver.query.get_or_404(waiver_id)
    form = WaiverForm(obj=waiver)
    if form.validate_on_submit():
        form.populate_obj(waiver)
        waiver.updated_date = datetime.utcnow()
        waiver.updated_by = current_user.id
        db.session.commit()
        flash('Waiver updated successfully.', 'success')
        return redirect(url_for('waivers.view_waiver', waiver_id=waiver.id))
    return render_template('waivers/waiver_form.html', form=form)


# Waiver - User Login - View and Sign Waiver
@waiver_bp.route('waivers/<int:waiver_id>',
                 methods=['GET', 'POST'])
@login_required
def view_sign_waiver(waiver_id):
    """User will view and sign a waiver"""
    waiver = Waiver.query.get_or_404(waiver_id)
    form = WaiverAgreementForm()
    if form.validate_on_submit():
        waiver_agreement = WaiverAgreement()
        form.populate_obj(waiver_agreement)
        waiver_agreement.agreement_date = datetime.utcnow()
        waiver_agreement.waiver_id = waiver_id
        waiver_agreement.user_id = current_user.id
        db.session.add(waiver_agreement)
        db.session.commit()
        flash('Waiver signed successfully.', 'success')
        return redirect(url_for('waivers.view_waiver', waiver_id=waiver.id))
    return render_template('waivers/waiver_agreement.html', form=form,
                           waiver=waiver)
