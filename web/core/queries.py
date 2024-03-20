"""Database queries for the Core views"""
# Imports
from datetime import datetime, timedelta
from app import db
from notifications.models import Notification
from events.models import Event
from users.models import User


# Query - Get 5 most recent notifications
def get_recent_notifications():
    """Get 5 most recent notifications"""

    five_recent_notifications = (
        db.session.query(Notification.id,
                         Notification.title,
                         Notification.message,
                         Notification.status,
                         Notification.created_date,
                         User.first_name,
                         User.last_name)
        .join(User, Notification.created_by == User.id)
        .filter(Notification.status == "active")
        .order_by(Notification.created_date.desc())
        .limit(5)
        .all()
    )

    return five_recent_notifications


# Query - Get 5 upcoming events based on the current date
def get_upcoming_events():
    """Get 5 upcoming events based on the current date"""

    five_upcoming_events = (
        db.session.query(Event.id,
                         Event.title,
                         Event.description,
                         Event.start_date,
                         Event.start_time,
                         Event.start_timezone,
                         Event.created_date,
                         User.first_name,
                         User.last_name)
        .join(User, Event.created_by == User.id)
        .filter(Event.start_date >= datetime.now() - timedelta(days=1))
        .order_by(Event.start_date.asc())
        .limit(5)
        .all()
    )

    return five_upcoming_events
