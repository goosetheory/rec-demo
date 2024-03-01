import uuid
from datetime import datetime

from flask import Flask, request
from http import HTTPStatus
from flask_sqlalchemy import SQLAlchemy

from commands import commands
from services import RestaurantService, NoSuitableTableError
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
    '''
    Get restaurants for a given set of eaters at a given time.
    Expected request contains query parameters: 
        - eater_ids, one or more uuids representing eaters
        - start_time, an iso-formatted datetime string
    '''
    eater_ids = [uuid.UUID(eater_id) for eater_id in request.args.getlist('eater_ids')]
    start_time = datetime.fromisoformat(request.args.get('start_time'))
    if not start_time or not eater_ids:
        print(f'Invalid request: eater_ids={eater_ids}, start_time={start_time}')
        return None, HTTPStatus.BAD_REQUEST
    print(f'Getting restaurants for eaters {eater_ids} at {start_time}')

    available_restaurants = restaurant_service.get_restaurants(eater_ids, start_time)
    return {'restaurants': [restaurant.to_wire() for restaurant in available_restaurants]}


@app.route('/reservations', methods=['POST'])
def create_reservation():
    '''
    Create a reservation for a given eater at a given restaurant at a given time.
    Expected request contains json body:
        - eater_ids, a list of uuids representing the eaters
        - restaurant_id, a uuid representing the restaurant
        - start_time, an iso-formatted datetime string
    Note to Rec: scoped out input validation for now
    '''
    body = request.json
    eater_ids = [uuid.UUID(eater_id) for eater_id in body.get('eater_ids')]
    restaurant_id = uuid.UUID(body.get('restaurant_id'))
    start_time = datetime.fromisoformat(body.get('start_time'))

    print(f'Creating reservation for eaters {eater_ids} at {restaurant_id} at {start_time}')
    
    # Note to Rec: as mentioned in the spec, we're assuming this method is called right after
    # the GET /restaurants method, so we're (optimistically, incorrectly) not checking for
    # restaurant availability here.
    try:
        reservation = restaurant_service.create_reservation(eater_ids, restaurant_id, start_time)
    except NoSuitableTableError:
        return None, HTTPStatus.CONFLICT

    return reservation.to_wire()
