"""Create an RSS feed for events."""
# Imports
import pytz
from datetime import datetime, timedelta
from ics import Calendar, Event as IcsEvent
from flask import Blueprint, Response
import xml.etree.ElementTree as ET
from app import db
from users.models import User
from .models import Event

# Blueprint
rss_feed_bp = Blueprint('rss_feed', __name__)


# Routes and Views
@rss_feed_bp.route('/events/rss')
def events_feed():
    """Create an RSS feed for events."""

    events = (
        db.session.query(
            Event.id,
            Event.title,
            Event.description,
            Event.start_date,
            Event.start_time,
            Event.start_timezone,
            Event.event_status,
            Event.created_date,
            Event.updated_date,
            Event.event_leader_id,
            User.first_name,
            User.last_name
        )
        .join(User, Event.event_leader_id == User.id)
        .filter(Event.start_date >= datetime.now())
        .filter(Event.event_status == 'open')
        .order_by(Event.start_date.asc())
        .all()
    )

    rss = ET.Element('rss', version='2.0')
    channel = ET.SubElement(rss, 'channel')
    ET.SubElement(channel, 'title').text = 'OpenVolunteer Events Feed'
    ET.SubElement(channel, 'description').text = 'Upcoming events for OpenVolunteer'
    ET.SubElement(channel, 'lastBuildDate').text = datetime.now(pytz.utc).strftime('%a, %d %b %Y %H:%M:%S %z')

    for event in events:
        item = ET.SubElement(channel, 'item')
        ET.SubElement(item, 'guid').text = str(event.id)
        ET.SubElement(item, 'title').text = event.title
        description_text = f"{event.description}\n\nStart Date: {event.start_date.strftime('%a, %d %b %Y')}\nStart Time: {event.start_time.strftime('%H:%M %p')}\nTimezone: {event.start_timezone}\nCreated By: {event.first_name} {event.last_name}"
        ET.SubElement(item, 'description').text = description_text
        pubDate = datetime.combine(event.start_date, event.start_time).astimezone(pytz.timezone(event.start_timezone)).strftime('%a, %d %b %Y %H:%M:%S %Z')
        ET.SubElement(item, 'pubDate').text = pubDate

    rss_string = ET.tostring(rss, encoding='utf-8', method='xml')

    response = Response(rss_string, mimetype='application/rss+xml')

    return response


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
            User.first_name,
            User.last_name
        )
        .join(User, Event.event_leader_id == User.id)
        .filter(Event.start_date >= datetime.now())
        .filter(Event.event_status == 'open')
        .order_by(Event.start_date.asc())
        .all()
    )

    cal = Calendar()

    for event in events:
        # Combine date and time into a single datetime object
        start_datetime = datetime.combine(event.start_date, event.start_time)
        start_datetime = pytz.timezone(event.start_timezone).localize(start_datetime)
        end_datetime = datetime.combine(event.end_date, event.end_time)
        end_datetime = pytz.timezone(event.start_timezone).localize(end_datetime)

        # Create an event
        ical_event = IcsEvent()
        ical_event.name = event.title
        ical_event.begin = start_datetime
        ical_event.end = end_datetime
        ical_event.description = event.description
        ical_event.location = "Log into OpenVolunteer for location details"
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
