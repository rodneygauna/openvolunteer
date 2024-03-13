"""Functionality that allows users to send messages to each other."""
# Imports
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from .models import Message
from .forms import SendMessage
from .user_lookup import user_lookup


# Blueprint
messages_bp = Blueprint("messages", __name__)


# Route - Send Message
@login_required
@messages_bp.route("/messages/create", methods=["POST"])
def send_message():
    """Send a message to another user."""

    form = SendMessage()

    # Populate the select field with users
    form.message_to_id.choices = user_lookup()

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
