"""Create the database and the tables."""
import time
import os
from sqlalchemy import create_engine, inspect
from sqlalchemy.exc import OperationalError
from app import db, app

time.sleep(10)


with app.app_context():
    try:
        app.logger.info("Attempting to connect to the database...")
        engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
        connection = engine.connect()
        app.logger.info("Database connection successful.")

        # Check if database exists
        inspector = inspect(engine)
        databases = inspector.get_schema_names()
        if os.environ['POSTGRES_DB'] not in databases:
            app.logger.info("Database does not exist. Creating...")
            with app.app_context():
                db.create_all()
            app.logger.info("Database created successfully.")

        # If able to connect, check if the tables exist
        try:
            app.logger.info("Checking if tables exist...")
            inspector = inspect(engine)
            if not inspector.has_table('users'):
                app.logger.info("Tables do not exist. Creating...")
                with app.app_context():
                    db.create_all()
                app.logger.info("Tables created successfully.")
            else:
                app.logger.info("Tables exist.")
        except OperationalError as e:
            app.logger.error("Tables do not exist due to: %s", e)
            raise e
        except Exception as e_inner:
            app.logger.error("Database creation failed due to: %s", e_inner)
            raise e_inner
    except OperationalError as e:
        app.logger.error("Database connection failed due to: %s", e)
        raise e
