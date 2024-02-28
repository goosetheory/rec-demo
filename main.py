from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from commands import commands
from services import RestaurantService
from db import configure_db

app = Flask(__name__)

restaurant_service = RestaurantService()

configure_db(app)

app.register_blueprint(commands)

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    available_restaurants = restaurant_service.get_restaurants([], None)
    return {'restaurants': [restaurant.to_wire() for restaurant in available_restaurants]}