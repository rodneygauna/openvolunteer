"""Views for the notifications feature of the application."""
# Imports
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from users.models import User
from .models import Notification
from .forms import NotificationForm

# Blueprint
notifications_bp = Blueprint("notifications", __name__)


# Route - View Notifications
@notifications_bp.route("/notifications/view")
@login_required
def view_notifications():
    """View notifications route"""
    page = request.args.get('page', 1, type=int)
    notifications = (
        db.session.query(Notification.id,
                         Notification.title,
                         Notification.message,
                         Notification.status,
                         Notification.created_date,
                         User.first_name,
                         User.last_name)
        .join(User, Notification.created_by == User.id)
        .order_by(Notification.created_date.desc())
        .filter(Notification.status == "active")
        .order_by(Notification.created_date.desc())
        .paginate(page=page, per_page=5)
    )

    return render_template(
        "notifications/view.html", title="OpenVolunteer - Notifications",
        notifications=notifications)


# Route - Create Notification
@notifications_bp.route("/notifications/create", methods=["GET", "POST"])
@login_required
def create_notification():
    """Create notification route"""
    form = NotificationForm()

    if form.validate_on_submit():
        notification = Notification(
            title=form.title.data,
            message=form.message.data,
            created_by=current_user.id
        )

        db.session.add(notification)
        db.session.commit()

        flash("Notification created successfully", "success")
        return redirect(url_for("notifications.view_notifications"))

    return render_template("notifications/notification_form.html",
                           title="OpenVolunteer - Create Notification",
                           form=form)


# Route - Update Notification
@notifications_bp.route(
    "/notifications/edit/<int:notification_id>", methods=["GET", "POST"])
@login_required
def update_notification(notification_id):
    """Update notification route"""
    notification = Notification.query.get_or_404(notification_id)
    form = NotificationForm(obj=notification)

    if form.validate_on_submit():
        notification.title = form.title.data
        notification.message = form.message.data
        notification.status = form.status.data
        notification.updated_by = current_user.id
        notification.updated_date = datetime.utcnow()
        notification.updated_by = current_user.id

        db.session.commit()

        flash("Notification updated successfully", "success")
        return redirect(url_for("notifications.view_notifications"))

    return render_template("notifications/notification_form.html",
                           title="OpenVolunteer - Edit Notification",
                           form=form)


# Route - View Notification
@notifications_bp.route("/notifications/view/<int:notification_id>")
@login_required
def view_notification(notification_id):
    """View notification route"""

    CreatingUser = db.aliased(User, name="CreatingUser")
    UpdatingUser = db.aliased(User, name="UpdatingUser")

    notification = (
        db.session.query(Notification.id,
                         Notification.title,
                         Notification.message,
                         Notification.status,
                         Notification.created_date,
                         Notification.updated_date,
                         CreatingUser.first_name.label(
                             "created_by_first_name"),
                         CreatingUser.last_name.label("created_by_last_name"),
                         UpdatingUser.first_name.label(
                             "updated_by_first_name"),
                         UpdatingUser.last_name.label("updated_by_last_name"))
        .join(CreatingUser, Notification.created_by == CreatingUser.id)
        .outerjoin(UpdatingUser, Notification.updated_by == UpdatingUser.id)
        .filter(Notification.id == notification_id)
        .first_or_404()
    )

    return render_template(
        "notifications/view_notification.html",
        title="OpenVolunteer - View Notification",
        notification=notification)
