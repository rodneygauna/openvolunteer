"""
Flask app for the web interface of the project.
"""
from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from config import BaseConfig


# Flask app configuration
app = Flask(__name__)
app.config.from_object(BaseConfig)
db = SQLAlchemy(app)


# Importing models after db is defined
from users.models import *
from events.models import *
from notifications.models import *


# Flask-Login configuration
from login_config import login_manager
login_manager.init_app(app)
login_manager.login_view = 'users.login'


# Flak-Mail configuration
mail = Mail()
mail.init_app(app)


# Flask Blueprints - Imports
from users.views import users_bp
from core.views import core_bp
from events.views import event_bp
from events.rss_feed import rss_feed_bp
from notifications.views import notifications_bp
from messages.views import messages_bp

# Flask Blueprints - Register
app.register_blueprint(users_bp)
app.register_blueprint(core_bp)
app.register_blueprint(event_bp)
app.register_blueprint(notifications_bp)
app.register_blueprint(messages_bp)
app.register_blueprint(rss_feed_bp)


# Main run script
if __name__ == '__main__':
    app.run()
