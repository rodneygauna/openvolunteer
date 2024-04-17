"""Core > Views"""

# Imports
from flask import render_template, Blueprint
from .queries import (
    get_upcoming_events,
    get_recent_notifications,
    get_active_users_count,
    get_active_events_count,
    get_active_notifications_count,
    get_total_event_hours,
    get_organization_details
)


# Blueprint
core_bp = Blueprint('core', __name__)


# Home page
@core_bp.route('/')
def index():
    """Home page"""

    # Organization Name
    organization_name = get_organization_details()

    # Upcoming Events
    upcoming_events = get_upcoming_events()

    # Recent Notifications
    recent_notifications = get_recent_notifications()

    # Stat Counts
    users_count = get_active_users_count()
    events_count = get_active_events_count()
    notifications_count = get_active_notifications_count()
    event_hours_count = get_total_event_hours()

    return render_template('index.html',
                           title='OpenVoluteer - Home',
                           upcoming_events=upcoming_events,
                           recent_notifications=recent_notifications,
                           users_count=users_count,
                           events_count=events_count,
                           notifications_count=notifications_count,
                           event_hours_count=event_hours_count,
                           organization_name=organization_name)
