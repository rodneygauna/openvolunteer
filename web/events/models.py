"""Database models for the events feature of the application."""
# Imports
from datetime import datetime
from app import db


# Model - Event
class Event(db.Model):
    """Event model"""

    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    event_leader_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    max_attendees = db.Column(db.Integer, default=0)
    start_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    start_timezone = db.Column(db.Text, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey("locations.id"))
    event_status = db.Column(db.String(255), default="open")
    created_date = db.Column(db.DateTime, default=datetime.utcnow())
    created_by = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False)
    updated_date = db.Column(db.DateTime)
    updated_by = db.Column(db.Integer, db.ForeignKey("users.id"))


# Model - Event Attendee
class EventAttendee(db.Model):
    """Event Attendee model"""

    __tablename__ = "event_attendees"

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"))
    attendee_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    attendee_status = db.Column(db.String(255), nullable=False,
                                default="pending")
    comments = db.Column(db.Text)
    created_date = db.Column(db.DateTime, default=datetime.utcnow())
    created_by = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False)
    updated_date = db.Column(db.DateTime)
    updated_by = db.Column(db.Integer, db.ForeignKey("users.id"))
