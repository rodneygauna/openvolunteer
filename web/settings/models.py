"""Database models for settings and other configurations."""
# Imports
from datetime import datetime
from app import db


# Model - Foundation
class Foundation(db.Model):
    """Foundation model"""

    __tablename__ = "foundation"

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
    created_date = db.Column(db.DateTime, default=datetime.utcnow())
    created_by = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False)
    updated_date = db.Column(db.DateTime)
    updated_by = db.Column(db.Integer, db.ForeignKey("users.id"))


# Model - Default Preferences
class DefaultPreference(db.Model):
    """Default Preference model"""

    __tablename__ = "default_preferences"

    id = db.Column(db.Integer, primary_key=True)
    default_timezone = db.Column(db.String(255))
    enable_2fa = db.Column(db.Boolean)
    created_date = db.Column(db.DateTime, default=datetime.utcnow())
    created_by = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False)
    updated_date = db.Column(db.DateTime)
    updated_by = db.Column(db.Integer, db.ForeignKey("users.id"))


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
    comments = db.Column(db.Text)
    created_date = db.Column(db.DateTime, default=datetime.utcnow())
    created_by = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False)
    updated_date = db.Column(db.DateTime)
    updated_by = db.Column(db.Integer, db.ForeignKey("users.id"))
