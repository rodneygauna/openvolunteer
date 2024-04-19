"""Database queries for reports."""
# Imports
from sqlalchemy.orm import aliased
from app import db
from events.models import Event, EventAttendee
from users.models import User
from waivers.models import Waiver, WaiverAgreement


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
        db.session.query(
            Event.id,
            Event.title,
            Event.start_date,
            Event.start_time,
            Event.start_timezone,
            Event.event_status,
            EventAttendee.attendee_status)
        .join(EventAttendee, EventAttendee.event_id == Event.id)
        .filter(EventAttendee.attendee_id == user_id)
        .filter(EventAttendee.attendee_status.in_(
            ["pending", "confirmed", "accepted", "standby"]))
        .order_by(Event.start_date.desc(), Event.start_time.desc())
        .all()
    )
    return events


# Function - Return a list of all waivers signed by the user
def user_waivers(user_id):
    """Query all waivers signed by a user."""
    waivers = (
        db.session.query(
            Waiver.id,
            Waiver.version,
            WaiverAgreement.agreement_date,
            WaiverAgreement.signee_first_name,
            WaiverAgreement.signee_last_name,
            WaiverAgreement.signee_date_of_birth)
        .join(WaiverAgreement, WaiverAgreement.waiver_id == Waiver.id)
        .filter(WaiverAgreement.user_id == user_id)
        .order_by(WaiverAgreement.agreement_date.desc())
        .all()
    )
    return waivers


# Function - Return a list of all users who signed a waiver
def waiver_signees(waiver_id):
    """Query all users who signed a waiver."""
    signees = (
        db.session.query(
            WaiverAgreement.waiver_id,
            WaiverAgreement.agreement_date,
            WaiverAgreement.signee_first_name,
            WaiverAgreement.signee_last_name,
            WaiverAgreement.signee_date_of_birth,
            WaiverAgreement.user_id,
            User.id,
            User.first_name,
            User.last_name)
        .join(User, User.id == WaiverAgreement.user_id)
        .filter(WaiverAgreement.waiver_id == waiver_id)
        .order_by(WaiverAgreement.agreement_date.desc())
        .all()
    )
    return signees
