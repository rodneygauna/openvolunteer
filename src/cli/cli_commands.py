"""CLI Commands for the app"""


# Imports
from faker import Faker
from flask import Blueprint
from werkzeug.security import generate_password_hash
from src import db
from src.users.models import User


# Faker instance
faker = Faker()


# Blueprint initialization
commands_bp = Blueprint("commands", __name__)


# Flask CLI Commands
@commands_bp.cli.command("db_create")
def db_create():
    """Creates the database using SQLAlchemy"""
    db.create_all()
    print("Database created!")


@commands_bp.cli.command("db_drop")
def db_drop():
    """Drops the database using SQLAlchemy"""
    db.drop_all()
    print("Database dropped!")


@commands_bp.cli.command("db_seed")
def db_seed():
    """Seeds the database"""

    # Variable for the maximum range
    max_range = 10
    # Data to seed the database with
    data = []

    # Create users
    for _ in range(1, max_range+1):
        data.append(
            User(
                email=faker.email(),
                password_hash=generate_password_hash("password")
            )
        )

    # Add the data to the database
    for entry in data:
        db.session.add(entry)
    db.session.commit()
    print("Database seeded!")
