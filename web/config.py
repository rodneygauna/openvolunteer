"""
Basic configuration file for the application.
Variables are read from the environment variables from docker-compose.yml
"""
import os


class BaseConfig(object):
    """Base configuration for the application."""
    # Database configuration
    DB_NAME = os.environ['POSTGRES_DB']
    DB_USER = os.environ['POSTGRES_USER']
    DB_PASS = os.environ['POSTGRES_PASSWORD']
    DB_PORT = os.environ['DATABASE_PORT']
    SQLALCHEMY_DATABASE_URI = (
        f'postgresql://{DB_USER}:{DB_PASS}@postgres:{DB_PORT}/{DB_NAME}'
    )
    # Flask-Mail configuration
    MAIL_SERVER = os.environ['MAIL_SERVER']
    MAIL_PORT = os.environ['MAIL_PORT']
    MAIL_USE_TLS = os.environ['MAIL_USE_TLS'].lower() == 'true'
    MAIL_USE_SSL = os.environ['MAIL_USE_SSL'].lower() == 'true'
    MAIL_USERNAME = os.environ['MAIL_USER']
    MAIL_PASSWORD = os.environ['MAIL_PASSWORD']
    # Encryption key
    SECRET_KEY = os.environ['SECRET_KEY']
    # SSL configuration
    SSL_CERT_PATH = os.environ['SSL_CERT_PATH']
    SSL_KEY_PATH = os.environ['SSL_KEY_PATH']
    SSL_CONTEXT = (SSL_CERT_PATH, SSL_KEY_PATH)
