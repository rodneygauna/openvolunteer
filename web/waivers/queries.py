"""Function helpers for querying the database for waiver data."""
# Imports
from sqlalchemy.orm import aliased
from app import db
from users.models import User
from .models import Waiver


# Function - Get Waivers
def get_waivers(waiver_id=None):
    """Get waivers from the database. If waiver_id is provided,
    return a single waiver."""
    created_by_user = aliased(User)
    updated_by_user = aliased(User)
    query = (
        db.session.query(
            Waiver.id,
            Waiver.active_date,
            Waiver.expiration_date,
            Waiver.version,
            Waiver.created_date,
            Waiver.updated_date,
            created_by_user.first_name.label('created_by_first_name'),
            created_by_user.last_name.label('created_by_last_name'),
            updated_by_user.first_name.label('updated_by_first_name'),
            updated_by_user.last_name.label('updated_by_last_name'),
        )
        .join(created_by_user, Waiver.created_by == created_by_user.id)
        .outerjoin(updated_by_user, Waiver.updated_by == updated_by_user.id)
    )
    if waiver_id is not None:
        return query.filter(Waiver.id == waiver_id).first()
    else:
        return query.all()
