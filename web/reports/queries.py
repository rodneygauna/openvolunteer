"""Database queries for reports."""
# Imports
from app import db
from events.models import Event, EventAttendee


# Function - Single User Total Volunteer Hours
def single_user_total_volunteer_hours(user_id, from_date, to_date):
    """Query total volunteer hours for a single user."""
    total_hours = (
        db.session.query(db.func.sum(Event.end_time - Event.start_time))
        .join(EventAttendee, EventAttendee.event_id == Event.id)
        .filter(EventAttendee.user_id == user_id)
        .filter(Event.start_date >= from_date)
        .filter(Event.end_date <= to_date)
        .filter(EventAttendee.attendee_status.in_(["confirmed", "accepted"]))
        .scalar()
    )
    return total_hours


# Function - Return a list of all events the user signed up for
def user_events(user_id):
    """Query all events a user signed up for."""
    events = (
        db.session.query(Event)
        .join(EventAttendee, EventAttendee.event_id == Event.id)
        .filter(EventAttendee.attendee_id == user_id)
        .filter(EventAttendee.attendee_status.in_(
            ["pending", "confirmed", "accepted", "standby"]))
        .all()
    )
    return events
