"""
Views for the Event app.
"""
# Imports
from datetime import datetime
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_required, current_user
from sqlalchemy import or_
from app import db
from users.models import User
from .forms import EventForm, EventSignupForm
from .models import Event, EventAttendee


# Blueprint
event_bp = Blueprint("events", __name__)


# View Event
@login_required
@event_bp.route("/view_events")
def view_events():
    """View all Event"""

    today = datetime.now().date()
    page = request.args.get('page', 1, type=int)
    event_info = db.session.query(
        Event.id,
        Event.start_date,
        Event.start_time,
        Event.start_timezone,
        Event.end_date,
        Event.end_time,
        Event.title,
        Event.description,
        Event.max_attendees,
        Event.event_status,
        Event.updated_date,
        db.func.count(EventAttendee.attendee_id).label("attendee_count"),
    )\
        .join(User, Event.event_leader_id == User.id)\
        .outerjoin(EventAttendee, db.and_(
            Event.id == EventAttendee.event_id,
            EventAttendee.attendee_status.in_(
                ["pending", "accepted", "standby", "confirmed"]
            )))\
        .filter(Event.start_date >= today, Event.event_status == "open")\
        .group_by(Event.id)\
        .order_by(Event.start_date.asc(), Event.start_time.asc())\
        .paginate(page=page, per_page=5)

    return render_template(
        "events/view_events.html",
        title="OpenVolunteer - View Event",
        event_info=event_info)


# View event
@event_bp.route("/event/<int:event_id>")
@login_required
def event(event_id):
    """View an event's details"""

    event = Event.query.get_or_404(event_id)
    event_details = db.session.query(
        Event.id,
        Event.start_date,
        Event.start_time,
        Event.start_timezone,
        Event.end_date,
        Event.end_time,
        Event.title,
        Event.description,
        Event.max_attendees,
        Event.event_status,
        Event.updated_date,
        User.first_name,
        User.last_name
        )\
        .join(User, Event.event_leader_id == User.id)\
        .filter(Event.id == event_id).first()
    event_roster = db.session.query(EventAttendee.id,
                                    EventAttendee.attendee_id,
                                    EventAttendee.comments,
                                    EventAttendee.attendee_status,
                                    User.first_name,
                                    User.last_name)\
        .join(User, EventAttendee.attendee_id == User.id)\
        .filter(EventAttendee.event_id == event_id)\
        .order_by(EventAttendee.updated_date.asc()).all()

    # Check if current user is in roster and if they have canceled
    current_user_in_roster = False
    current_user_canceled = False
    current_user_is_leader = False

    if event.event_leader_id == current_user.id:
        current_user_is_leader = True

    for attendee in event_roster:
        if attendee.attendee_id == current_user.id:
            current_user_in_roster = True
            if attendee.attendee_status == "canceled":
                current_user_canceled = True

    return render_template(
        "events/event.html",
        title="OpenVolunteer - View Event",
        event=event,
        event_details=event_details,
        event_roster=event_roster,
        current_user_in_roster=current_user_in_roster,
        current_user_canceled=current_user_canceled,
        current_user_is_leader=current_user_is_leader)


# Create event
@ event_bp.route("/create_event", methods=["GET", "POST"])
@ login_required
def create_event():
    """Creates a new event"""

    form = EventForm()

    if form.validate_on_submit():
        if form.start_date.data is None:
            print("start_date is None")

        new_event = Event(
            event_leader_id=current_user.id,
            start_date=form.start_date.data,
            start_time=form.start_time.data,
            start_timezone=form.start_timezone.data,
            end_date=form.end_date.data,
            end_time=form.end_time.data,
            title=form.title.data,
            description=form.description.data,
            max_attendees=form.max_attendees.data,
            event_status="open",
            created_by=current_user.id)

        db.session.add(new_event)
        db.session.commit()

        flash("Event created successfully.", "success")
        return redirect(url_for("events.event", event_id=new_event.id))

    return render_template(
        "events/create_event.html",
        title="OpenVolunteer - Create Event",
        form=form
    )


# Edit event
@ event_bp.route("/edit_event/<int:event_id>", methods=["GET", "POST"])
@ login_required
def edit_event(event_id):
    """Edits an existing event"""

    event = Event.query.get_or_404(event_id)

    if event.event_leader_id != current_user.id:
        flash("You are not authorized to edit this event.", "danger")
        return redirect(url_for("events.view_Event"))

    form = EventForm()

    if form.validate_on_submit():
        event.start_date = form.start_date.data
        event.start_time = form.start_time.data
        event.start_timezone = form.start_timezone.data
        event.end_date = form.end_date.data
        event.end_time = form.end_time.data
        event.title = form.title.data
        event.description = form.description.data
        event.max_attendees = form.max_attendees.data
        event.event_status = form.event_status.data
        event.updated_date = datetime.utcnow()
        event.updated_by = current_user.id

        db.session.commit()
        flash("Event updated successfully.", "success")
        return redirect(url_for("events.event", event_id=event.id))

    elif request.method == "GET":
        form.start_date.data = event.start_date
        form.start_time.data = event.start_time
        form.start_timezone.data = event.start_timezone
        form.end_date.data = event.end_date
        form.end_time.data = event.end_time
        form.title.data = event.title
        form.description.data = event.description
        form.max_attendees.data = event.max_attendees
        form.event_status.data = event.event_status

    return render_template(
        "events/edit_event.html",
        title="OpenVolunteer - Edit Event",
        form=form
    )


# Sign up for event
@ event_bp.route("/sign_up/<int:event_id>", methods=["GET", "POST"])
@ login_required
def event_signup(event_id):
    """Sign up for the event"""

    form = EventSignupForm()

    event = Event.query.get_or_404(event_id)

    # Logic to determine the attendee's status
    # Count how many active attendees are in the roster
    roster_active_count = EventAttendee.query.filter_by(
        event_id=event_id).filter(
        or_(EventAttendee.attendee_status == "pending",
            EventAttendee.attendee_status == "accepted",
            EventAttendee.attendee_status == "confirmed")).count()
    # Max number of attendees allowed in the event
    max_allowed = event.max_attendees
    if roster_active_count >= max_allowed:
        attendee_status = "standby"
    else:
        attendee_status = "pending"

    if event.event_status != "open":
        flash("This event is not open for signups.", "danger")

    if event.event_leader_id == current_user.id:
        flash("You are the leader of this event.", "danger")

    if form.validate_on_submit():
        event_signup = EventAttendee(
            event_id=event_id,
            attendee_id=current_user.id,
            comments=form.comments.data,
            attendee_status=attendee_status,
            created_by=current_user.id,
            created_date=datetime.utcnow()
        )

        db.session.add(event_signup)
        db.session.commit()
        flash("You have signed up for the event.", "success")
        return redirect(url_for("events.event", event_id=event_id))

    return render_template("events/event_signup.html",
                           title="OpenVolunteer - Event Signup",
                           form=form)


# Edit event signup
@ event_bp.route("/edit_event_signup/<int:event_id>", methods=["GET", "POST"])
@ login_required
def edit_event_signup(event_id):
    """Edit event signup"""

    form = EventSignupForm()

    event = Event.query.get_or_404(event_id)

    if event.event_status != "open":
        flash("This event is not open for signups.", "danger")

    if event.event_leader_id == current_user.id:
        flash("You are the leader of this event.", "danger")

    event_signup = EventAttendee.query.filter_by(
        event_id=event_id, attendee_id=current_user.id).first()

    if form.validate_on_submit():
        event_signup.comments = form.comments.data
        event_signup.updated_date = datetime.utcnow()
        event_signup.updated_by = current_user.id

        if event_signup.attendee_status == "canceled":
            event_signup.attendee_status = "pending"

        db.session.commit()
        flash("You have updated your event signup.", "success")
        return redirect(url_for("events.event", event_id=event_id))

    elif request.method == "GET":
        form.comments.data = event_signup.comments

    return render_template("events/event_signup.html",
                           title="OpenVolunteer - Edit Event Signup",
                           form=form)


# Cancel event signup
@ event_bp.route("/cancel_event_signup/<int:event_id>",
                 methods=["GET", "POST"])
@ login_required
def cancel_event_signup(event_id):
    """Changes event status to canceled"""

    event = Event.query.get_or_404(event_id)

    if event.event_status != "open":
        flash("This event is not open for signups.", "danger")

    if event.event_leader_id == current_user.id:
        flash("You are the leader of this event.", "danger")

    event_signup = EventAttendee.query.filter_by(
        event_id=event_id, attendee_id=current_user.id).first()

    if event_signup:
        event_signup.attendee_status = "canceled"
        event_signup.updated_date = datetime.utcnow()
        event_signup.updated_by = current_user.id

        db.session.commit()
        flash("You have deleted your event signup.", "success")
    else:
        flash("You are not signed up for this event.", "danger")

    return redirect(url_for("events.event", event_id=event_id))
