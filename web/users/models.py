"""Base database models for the application."""
# Imports
from datetime import datetime
from flask import redirect, url_for
from werkzeug.security import check_password_hash
from flask_login import UserMixin
from login_config import login_manager
from app import db


# Login Manager - User Loader
@login_manager.user_loader
def load_user(user_id):
    """Loads the user from the database"""
    return User.query.get(int(user_id))


# Login Manager - Unauthorized Handler
@login_manager.unauthorized_handler
def unauthorized():
    """Redirects unauthorized users to the login page"""
    return redirect(url_for("users.login"))


# Model - User
class User(db.Model, UserMixin):
    """User model"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, index=True)
    phone = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255))
    role = db.Column(db.String(255), default="user")
    status = db.Column(db.String(255), default="active")
    created_date = db.Column(db.DateTime, default=datetime.utcnow())
    updated_date = db.Column(db.DateTime)

    def __init__(self, first_name, last_name, email, phone, password_hash):
        """Initializes the user"""
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.password_hash = password_hash

    def check_password(self, password):
        """Checks if the password is correct"""
        return check_password_hash(self.password_hash, password)
