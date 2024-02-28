from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from commands import commands

from db import configure_db

app = Flask(__name__)

configure_db(app)

app.register_blueprint(commands)

@app.route('/')
def index():
    return 'Hello, World!'

