"""Database queries and functions for settings and other configurations."""
# Imports
from app import db
from users.models import User


# Function - Get Users
def get_users():
    """Get all users."""
    users = db.session.query(
        User.id, User.first_name, User.last_name,
        User.email, User.role, User.status
    )\
        .filter_by(status="active")\
        .order_by(User.first_name)\
        .all()

    return users
