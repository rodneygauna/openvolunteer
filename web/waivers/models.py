"""Database models for the waivers feature of the application."""
# Imports
from datetime import datetime
from app import db


# Model - Waiver
class Waiver(db.Model):
    """Waiver model"""

    __tablename__ = "waivers"

    id = db.Column(db.Integer, primary_key=True)
    active_date = db.Column(db.Date, nullable=False)
    expiration_date = db.Column(db.Date)
    version = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    signature_consent = db.Column(db.Text, default=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow())
    created_by = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False)
    updated_date = db.Column(db.DateTime)
    updated_by = db.Column(db.Integer, db.ForeignKey("users.id"))


# Model - Waiver Agreement
class WaiverAgreement(db.Model):
    """Waiver Agreement model"""

    __tablename__ = "waiver_agreements"

    id = db.Column(db.Integer, primary_key=True)
    waiver_id = db.Column(db.Integer, db.ForeignKey("waivers.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    agreement_date = db.Column(db.Date, default=datetime.utcnow())
    signee_first_name = db.Column(db.String(255), nullable=False)
    signee_last_name = db.Column(db.String(255), nullable=False)
    signee_date_of_birth = db.Column(db.Date, nullable=False)
