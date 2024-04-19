"""Create the database and the tables."""
import time
import os
from sqlalchemy import create_engine, inspect
from sqlalchemy.exc import OperationalError
from app import db, app

time.sleep(5)


with app.app_context():
    db.create_all()
