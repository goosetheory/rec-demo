import uuid

from datetime import datetime, timedelta

from sqlalchemy import func
from sqlalchemy.orm import joinedload
from db import session_scope, Restaurant, Diet, Table, Eater


class RestaurantService:
    RESERVATION_LENGTH = timedelta(minutes=120)

    def get_restaurants(self, eater_ids, start_time):
        with session_scope() as session:
            # Get diets for eaters
            diets = session.query(Diet) \
                .join(Diet.eaters) \
                .filter(Eater.id.in_(eater_ids)) \
                .all()

            # Subquery to count the number of matching diets for each restaurant
            # (We require all provided diets to be matched)
            matching_diets_subq = session.query(Restaurant.id, func.count(Diet.id).label('diet_count')) \
                .join(Restaurant.endorsements) \
                .filter(Diet.id.in_([diet.id for diet in diets])) \
                .group_by(Restaurant.id) \
                .having(func.count(Diet.id) == len(diets)) \
                .subquery()

            # Restaurants with matching diets and tables that can accommodate eaters
            restaurants = session.query(Restaurant) \
                .join(matching_diets_subq, Restaurant.id == matching_diets_subq.c.id) \
                .options(joinedload(Restaurant.tables), joinedload(Restaurant.endorsements)) \
                .filter(Restaurant.tables.any(Table.capacity >= len(eater_ids))) \
                .all()

            print(f'Restaurants: {[r.name for r in restaurants]}')
            


            # Get existing reservations for restaurants, filter

            return restaurants

