"""Create the database and the tables."""
import time
from app import db, app

time.sleep(10)


with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        print(f"An error occurred: {e}")
