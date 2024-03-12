"""Database models for the notifications feature of the application."""
# Imports
from datetime import datetime
from app import db


# Model - Notification
class Notification(db.Model):
    """Notification model"""

    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), nullable=False, default="active")
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False)
    updated_date = db.Column(db.DateTime)
    updated_by = db.Column(db.Integer, db.ForeignKey("users.id"))
