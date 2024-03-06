"""Base database models for the application."""
from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import Enum
from app import db


class Status(PyEnum):
    """Enum for status"""
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class BaseModel(db.Model):
    """Base model for all models"""

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_date = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)
    updated_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    updated_date = db.Column(db.DateTime)
    status = db.Column(Enum(Status), default=Status.ACTIVE)
