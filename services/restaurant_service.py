from sqlalchemy.orm import joinedload
from db import session_scope, Restaurant


class RestaurantService:
    def get_restaurants(self, user_ids, start_time):
        with session_scope() as session:
            
            restaurants = session.query(Restaurant) \
                .options(joinedload(Restaurant.tables), joinedload(Restaurant.endorsements)) \
                .all()

            return restaurants
