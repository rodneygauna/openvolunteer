"""
Flask app for the web interface of the project.
"""
from flask import Flask
from flask_mail import Mail
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from config import BaseConfig


# Flask app configuration
app = Flask(__name__)
app.config.from_object(BaseConfig)
db = SQLAlchemy(app)


# Importing models after db is defined
from models import *


# Flask-Login configuration
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login'


# Flak-Mail configuration
mail = Mail()
mail.init_app(app)


# Main run script
if __name__ == '__main__':
    app.run()
