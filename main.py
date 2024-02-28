import uuid

from flask import Flask, request
from http import HTTPStatus
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
    eater_ids = request.args.getlist('eater_ids')
    eater_ids = [uuid.UUID(eater_id) for eater_id in eater_ids]
    start_time = request.args.get('start_time')
    if not start_time or not eater_ids:
        print(f'Invalid request: eater_ids={eater_ids}, start_time={start_time}')
        return None, HTTPStatus.BAD_REQUEST
    print(f'Getting restaurants for eaters {eater_ids} at {start_time}')

    available_restaurants = restaurant_service.get_restaurants(eater_ids, start_time)
    return {'restaurants': [restaurant.to_wire() for restaurant in available_restaurants]}