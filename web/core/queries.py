"""Database queries for the Core views"""
# Imports
from datetime import datetime, timedelta
from app import db
from notifications.models import Notification
from events.models import Event
from users.models import User
from settings.models import Organization


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


# Query - Total count of active users
def get_active_users_count():
    """Get total count of active users"""

    active_users_count = User.query.filter_by(status="active").count()

    return active_users_count


# Query - Total count of active events
def get_active_events_count():
    """Get total count of active events"""

    active_events_count = Event.query.filter_by(event_status="open").count()

    return active_events_count


# Query - Total count of active notifications
def get_active_notifications_count():
    """Get total count of active notifications"""

    active_notifications_count = Notification.query.filter_by(
        status="active").count()

    return active_notifications_count


# Query - Total count of event hours
def get_total_event_hours():
    """Get total count of event hours"""

    total_event_hours = (
        db.session.query(Event.id,
                         Event.start_date,
                         Event.start_time,
                         Event.end_date,
                         Event.end_time
                         )
        .filter(Event.end_date <= datetime.now())
        .all()
    )

    total_hours = 0
    for event in total_event_hours:
        start_datetime = datetime.combine(event.start_date, event.start_time)
        end_datetime = datetime.combine(event.end_date, event.end_time)
        duration = end_datetime - start_datetime
        total_hours += duration.total_seconds() / 3600

    return total_hours


# Query - Get organization details
def get_organization_details():
    """Get organization details"""

    organization = Organization.query.first()

    return organization
