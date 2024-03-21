"""Database models for settings and other configurations."""
# Imports
from datetime import datetime
from app import db


# Model - Organization
class Organization(db.Model):
    """Organization model"""

    __tablename__ = "organizations"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    fax = db.Column(db.String(255))
    address_1 = db.Column(db.String(255))
    address_2 = db.Column(db.String(255))
    city = db.Column(db.String(255))
    state = db.Column(db.String(255))
    postal_code = db.Column(db.String(255))
    maiLing_address_1 = db.Column(db.String(255))
    mailing_address_2 = db.Column(db.String(255))
    mailing_city = db.Column(db.String(255))
    mailing_state = db.Column(db.String(255))
    mailing_postal_code = db.Column(db.String(255))
    created_date = db.Column(
        db.DateTime, default=datetime.utcnow(), nullable=False)
    created_by = db.Column(
        db.Integer, db.ForiegnKey("users.id"), nullable=False)
    updated_date = db.Column(db.DateTime)
    udpated_by = db.Column(db.Integer, db.ForiegnKey("users.id"))


# Model - Default Preferences
class DefaultPreference(db.Model):
    """Default Preference model"""

    __tablename__ = "default_preferences"

    id = db.Column(db.Integer, primary_key=True)
    default_timezone = db.Column(db.String(255), default="UTC")


# Model - Locations
class Location(db.Model):
    """Location model"""

    __tablename__ = "locations"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    short_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    fax = db.Column(db.String(255))
    address_1 = db.Column(db.String(255))
    address_2 = db.Column(db.String(255))
    city = db.Column(db.String(255))
    state = db.Column(db.String(255))
    postal_code = db.Column(db.String(255))
    maiLing_address_1 = db.Column(db.String(255))
    mailing_address_2 = db.Column(db.String(255))
    mailing_city = db.Column(db.String(255))
    mailing_state = db.Column(db.String(255))
    mailing_postal_code = db.Column(db.String(255))
    created_date = db.Column(
        db.DateTime, default=datetime.utcnow(), nullable=False)
    created_by = db.Column(
        db.Integer, db.ForiegnKey("users.id"), nullable=False)
    updated_date = db.Column(db.DateTime)
    udpated_by = db.Column(db.Integer, db.ForiegnKey("users.id"))
