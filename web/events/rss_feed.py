"""Create an RSS feed for events."""
# Imports
from datetime import datetime
import pytz
from ics import Calendar, Event as IcsEvent
from flask import Blueprint, Response
from app import db
from users.models import User
from settings.models import Location
from .models import Event

# Blueprint
rss_feed_bp = Blueprint('rss_feed', __name__)


# calendar.ics route
@rss_feed_bp.route('/events/ics')
def events_ics():
    """Create an iCal feed for events."""

    events = (
        db.session.query(
            Event.id,
            Event.title,
            Event.description,
            Event.start_date,
            Event.start_time,
            Event.end_date,
            Event.end_time,
            Event.start_timezone,
            Event.event_status,
            Event.created_date,
            Event.updated_date,
            Event.event_leader_id,
            Event.location_id,
            Location.name.label('location_name'),
            Location.address_1.label('location_address_1'),
            Location.address_2.label('location_address_2'),
            Location.city.label('location_city'),
            Location.state.label('location_state'),
            Location.postal_code.label('location_postal_code'),
            User.first_name,
            User.last_name
        )
        .join(User, Event.event_leader_id == User.id)
        .outerjoin(Location, Event.location_id == Location.id)
        .filter(Event.start_date >= datetime.now())
        .filter(Event.event_status == 'open')
        .order_by(Event.start_date.asc())
        .all()
    )

    cal = Calendar()

    for event in events:
        # Combine date and time into a single datetime object
        start_datetime = datetime.combine(event.start_date, event.start_time)
        start_datetime = pytz.timezone(
            event.start_timezone).localize(start_datetime)
        end_datetime = datetime.combine(event.end_date, event.end_time)
        end_datetime = pytz.timezone(
            event.start_timezone).localize(end_datetime)

        # Combine location details into a single string
        if event.location_id:
            location = (
                f"{event.location_address_1}, {event.location_city}, {event.location_state} {event.location_postal_code}"
            )
            if event.location_address_2:
                location = (
                    f"{event.location_address_1}, {event.location_address_2}, {event.location_city}, {event.location_state} {event.location_postal_code}"
                )
        else:
            location = "See event description for location details."

        # Create an event
        ical_event = IcsEvent()
        ical_event.name = event.title
        ical_event.begin = start_datetime
        ical_event.end = end_datetime
        ical_event.description = event.description
        ical_event.location = location
        ical_event.created = event.created_date
        ical_event.last_modified = event.updated_date
        ical_event.uid = str(event.id)

        # Add the event to the calendar
        cal.events.add(ical_event)

    # Convert the calendar to a string in iCalendar format
    ical_str = str(cal)

    # Return the iCalendar string as a response
    response = Response(ical_str, mimetype='text/calendar')
    response.headers["Content-Disposition"] = "attachment; filename=events.ics"

    return response
