import pytest
from flask_migrate import upgrade, Migrate
from flask import Flask
from sqlalchemy.sql import text
from sqlalchemy import create_engine

from db import db, configure_db

@pytest.fixture(scope='session', autouse=True)
def app():
    # Create an app, including a test db from the latest migration...
    app = _setup_app()

    yield app

    # ...then destroy it, including resetting the test db.
    _teardown_app(app)


@pytest.fixture()
def db_session(app):
    with app.app_context():
        with db.session_scope() as session:
            yield session


def _setup_app():
    # TODO: set up temp db as part of test setup, rather than expecting existing
    # (which will be modified heavily by tests)
    test_db_creds = {
        'username': 'postgres',
        'password': 'postgres',
        'host': 'localhost',
        'port': '5432',
        'dbname': 'postgres'
    }

    app = Flask(__name__)
    app.config['TESTING'] = True

    with app.app_context():
        configure_db(app)
        Migrate(app, db)
        upgrade()

    return app


def _teardown_app(app):
    with app.app_context():
        engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
        with engine.begin() as conn:
            cleanup_query = '''
                DROP SCHEMA IF EXISTS public CASCADE;
                CREATE SCHEMA public;
                GRANT ALL ON SCHEMA public TO postgres;
                GRANT ALL ON SCHEMA public TO public;
            '''
            conn.execute(text(cleanup_query))
