"""Logic for looking up a user by their first name, last name, or email."""
# Imports
from users.models import User


# Lookup User
def lookup_user():
    """Lookup a user by their user ID."""
    # Lookup the the user by first name, last name, or email
    user = User.query.filter_by(
        User.status == "active").order_by(User.first_name).all()

    return user.id, user.first_name, user.last_name
