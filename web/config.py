"""
Basic configuration file for the application.
"""
import os


with open(os.environ['POSTGRES_USER_FILE'], encoding='utf-8') as f:
    _db_user = f.read()

with open(os.environ['POSTGRES_PASSWORD_FILE'], encoding='utf-8') as f:
    _db_pass = f.read()

with open(os.environ['MAIL_USER_FILE'], encoding='utf-8') as f:
    _mail_user = f.read()

with open(os.environ['MAIL_PASSWORD_FILE'], encoding='utf-8') as f:
    _mail_pass = f.read()


class BaseConfig(object):
    """Base configuration for the application."""
    DB_NAME = os.environ['POSTGRES_DB']
    DB_USER = _db_user
    DB_PASS = _db_pass
    DB_PORT = os.environ['DATABASE_PORT']
    SQLALCHEMY_DATABASE_URI = (
        f'postgresql://{DB_USER}:{DB_PASS}@postgres:{DB_PORT}/{DB_NAME}'
    )
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = os.environ['MAIL_PORT']
    MAIL_USE_TLS = os.environ['MAIL_USE_TLS']
    MAIL_USE_SSL = os.environ['MAIL_USE_SSL']
    MAIL_USERNAME = 'rodneygauna@gmail.com'
    MAIL_PASSWORD = 'password'
    # MAIL_USERNAME = _mail_user
    # MAIL_PASSWORD = _mail_pass
