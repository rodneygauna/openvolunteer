"""Organization models."""
# Imports
from datetime import datetime
from app import db


# Model - Organizations
class Organizations(db.Model):
    """Organizations model"""

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
    created_date = db.Column(db.DateTime, default=datetime.utcnow())
    created_by = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False)
    updated_date = db.Column(db.DateTime)
    updated_by = db.Column(db.Integer, db.ForeignKey("users.id"))


# Model - Organization Users
class OrganizationUsers(db.Model):
    """Organization Users model -
    Many to Many relationship between organizations and users."""

    __tablename__ = "organization_users"

    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(
        db.Integer, db.ForeignKey("organizations.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    organization_user_role = db.Column(db.String(255),
                                       default="user", nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow())
    created_by = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False)
    updated_date = db.Column(db.DateTime)
    updated_by = db.Column(db.Integer, db.ForeignKey("users.id"))
