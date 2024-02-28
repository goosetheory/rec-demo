from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from contextlib import contextmanager

# Why isn't this whole file a class? Because db should be a singleton and we don't
# want to have to pass it around everywhere/use DI/make a singleton class
# for this simple demo app.

db = SQLAlchemy(session_options={"expire_on_commit": False})

def configure_db(app):
    # Such security, much wow
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/postgres'
    db.init_app(app)
    Migrate(app, db)


@contextmanager
def session_scope():
    session = db.session
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()