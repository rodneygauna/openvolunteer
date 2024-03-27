"""Decorator for admin or superuser access to views"""
# Imports
from functools import wraps
from flask import render_template
from flask_login import current_user


def superuser_required(f):
    """Decorator to check if user is a Super User or Admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role not in [
            "super user",
            "admin",
        ]:
            return render_template("40X.html",
                                   title="OpenVolunteer - 403 Unauthorized",
                                   error_code="403"), 403
        return f(*args, **kwargs)

    return decorated_function


def admin_required(f):
    """Decorator to check if user is an Admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role not in [
            "admin"
        ]:
            return render_template("40X.html",
                                   title="OpenVolunteer - 403 Unauthorized",
                                   error_code="403"), 403

        return f(*args, **kwargs)

    return decorated_function
