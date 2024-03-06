"""Initialization and configuration for the application."""


# Imports
import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from flask_login import LoginManager
from flask_mail import Mail


# Read .env file
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")

# Flask initialization
app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
# Database configuration using PostgreSQL
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True


# Database initialization
db = SQLAlchemy(app)


# Import models
from src.users.models import *


# Function to create the database if it doesn't exist
def create_database_if_not_exists():
    """Create the database if it doesn't exist."""
    try:
        engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
        engine.connect()
    except OperationalError as e:
        app.logger.error("Database connection failed due to: %s", e)
        app.logger.info("Attempting to create the database...")
        try:
            with app.app_context():
                db.create_all()
            app.logger.info("Database created successfully.")
        except Exception as e_inner:
            app.logger.error("Database creation failed due to: %s", e_inner)
            raise e_inner


# Login manager initialization
from src.login import login_manager
login_manager.init_app(app)
login_manager.login_view = "users.login"


# Mail configuration and initialization
mail = Mail()
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'rodneygauna@gmail.com'
app.config['MAIL_PASSWORD'] = EMAIL_PASSWORD
mail.init_app(app)


# Flask Blueprints - Imports
from src.cli.cli_commands import commands_bp
from src.core.views import core_bp
from src.users.views import users_bp

# Flask Blueprints - Register
app.register_blueprint(commands_bp)
app.register_blueprint(core_bp)
app.register_blueprint(users_bp)
