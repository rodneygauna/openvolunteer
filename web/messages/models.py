"""Database models for the messages feature of the application."""
# Imports
from datetime import datetime
from app import db


# Model - Message
class Message(db.Model):
    """Message model"""

    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    message_to_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False)
    message_from_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), nullable=False, default="unread")
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime)
