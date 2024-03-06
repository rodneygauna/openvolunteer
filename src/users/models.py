"""Users > Models"""

# Imports
from flask import redirect, url_for
from werkzeug.security import check_password_hash
from flask_login import UserMixin
from src import db
from src.login import login_manager
from src.models import BaseModel


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
class User(BaseModel, UserMixin):
    """User model"""

    __tablename__ = "users"

    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, index=True)
    password_hash = db.Column(db.String(255))
    profile_image = db.Column(
        db.String(255), nullable=False, default="default_profile.jpg"
    )
    role = db.Column(db.String(255), default="user")

    def __repr__(self):
        return f"User {self.email}"

    def check_password(self, password):
        """Checks if the password is correct"""
        return check_password_hash(self.password_hash, password)
