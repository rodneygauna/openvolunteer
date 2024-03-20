"""Core > Views"""

# Imports
from flask import render_template, Blueprint
from .queries import (
    get_upcoming_events,
    get_recent_notifications
)


# Blueprint
core_bp = Blueprint('core', __name__)


# Home page
@core_bp.route('/')
def index():
    """Home page"""

    # Upcoming Events
    upcoming_events = get_upcoming_events()

    # Recent Notifications
    recent_notifications = get_recent_notifications()

    return render_template('index.html',
                           title='OpenVoluteer - Home',
                           upcoming_events=upcoming_events,
                           recent_notifications=recent_notifications)
