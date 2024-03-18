"""Functionality that allows users to send messages to each other."""
# Imports
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from users.models import User
from .models import Message
from .forms import SendMessage

# Blueprint
messages_bp = Blueprint("messages", __name__)


# Route - Send Message
@login_required
@messages_bp.route("/messages/create", methods=["GET", "POST"])
def send_message():
    """Send a message to another user."""

    form = SendMessage()

    # Populate the select field with users
    active_users = (
        db.session.query(
            User.id,
            User.first_name,
            User.last_name,
            User.status
        )
        .filter(User.status == "active")
        .filter(User.id != current_user.id)
        .order_by(User.first_name)
        .all()
    )

    form.message_to_id.choices = [
        (user.id, f"{user.first_name} {user.last_name}")
        for user in active_users
    ]

    # Get the message data
    if form.validate_on_submit():
        message_to_id = form.message_to_id.data
        message = form.message.data

        # Create a new message
        new_message = Message(
            message_to_id=message_to_id,
            message_from_id=current_user.id,
            message=message
        )

        # Save the message to the database
        db.session.add(new_message)
        db.session.commit()

        # Flash message
        flash("Message sent!", "success")

        # Redirect to the messages page
        return redirect(url_for("messages.view_messages"))

    return render_template("messages/create.html", form=form)


# Route - View Messages
@login_required
@messages_bp.route("/messages")
def view_messages():
    """View messages for the current user."""

    # Get the messages
    page = request.args.get('page', 1, type=int)
    messages = (
        db.session.query(
            Message.id,
            Message.message,
            Message.status,
            Message.created_date,
            User.first_name.label("from_first_name"),
            User.last_name.label("from_last_name")
        )
        .join(User, User.id == Message.message_from_id)
        .filter(Message.message_to_id == current_user.id)
        .order_by(Message.created_date.desc())
        .paginate(page=page, per_page=10)
    )

    return render_template("messages/view.html", messages=messages)
