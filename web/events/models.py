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
    start_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    start_timezone = db.Column(db.Text, nullable=False)
    event_status = db.Column(db.String(255), default="active")
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False)
    updated_date = db.Column(db.DateTime)
    updated_by = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __init__(self, title, description, start_date, start_time,
                 start_timezone, created_by):
        """Initializes the event"""
        self.title = title
        self.description = description
        self.start_date = start_date
        self.start_time = start_time
        self.start_timezone = start_timezone
        self.created_by = created_by


# Model - Event Attendee
class EventAttendee(db.Model):
    """Event Attendee model"""

    __tablename__ = "event_attendees"

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"))
    attendee_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    status = db.Column(db.String(255), nullable=False, default="pending")
    comments = db.Column(db.Text)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False)
    updated_date = db.Column(db.DateTime)
    updated_by = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __init__(self, event_id, attendee_id, status, created_by):
        """Initializes the event attendee"""
        self.event_id = event_id
        self.attendee_id = attendee_id
        self.status = status
        self.created_by = created_by
