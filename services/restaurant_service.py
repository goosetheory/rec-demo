import uuid

from datetime import datetime, timedelta

from sqlalchemy import func, and_, select
from sqlalchemy.orm import joinedload
from db import session_scope, Restaurant, Diet, Table, Eater, Reservation


class RestaurantService:
    RESERVATION_LENGTH = timedelta(minutes=120)

    def get_restaurants(self, eater_ids, start_time):
        with session_scope() as session:
            restriction_friendly_restaurants = self._get_restriction_friendly_restaurants(
                session, eater_ids)

            print(f'Restriction-friendly restaurants: \
                    {[r.name for r in restriction_friendly_restaurants]}')
            
            open_restaurants = self._filter_restaurants_with_tables(
                session, restriction_friendly_restaurants, start_time, len(eater_ids))
            
            print(f'...with large-enough open tables: {[r.name for r in open_restaurants]}')

            # TODO: Should we be including table availability on these restaurants?
            return open_restaurants


    def _filter_restaurants_with_tables(self, session, restaurants, start_time, group_size):
        # Note to rec: these should be subqueries, but I've left them
        # separate for now for debugging purposes.
        # We're only interested in tables with space for all our eaters
        table_ids_without_enough_capacity = session.query(Table.id) \
            .filter(Table.restaurant_id.in_(restaurant.id for restaurant in restaurants)) \
            .filter(Table.capacity < group_size) \
            .all()

        # Can't book a reservation at a table if there's an overlapping reservation.
        # Here, we find tables that are booked.
        earliest_conflicting_reservation = start_time - self.RESERVATION_LENGTH
        latest_conflicting_reservation = start_time + self.RESERVATION_LENGTH
        large_enough_table_ids_without_overlapping_reservations = session.query(Table.id) \
            .filter(~Table.id.in_([t.id for t in table_ids_without_enough_capacity])) \
            .filter(Table.restaurant_id.in_(
                [restaurant.id for restaurant in restaurants])) \
            .filter(
                ~Table.reservations.any(
                    and_(
                        Reservation.start_time > earliest_conflicting_reservation,
                        Reservation.start_time < latest_conflicting_reservation
                    )
                )
            ) \
            .all()
        
        # Get tables at restriction-friendly restaurants with no conflicting reservations
        open_restaurants = session.query(Restaurant) \
            .join(Restaurant.tables) \
            .filter(Restaurant.id.in_(
                [restaurant.id for restaurant in restaurants])) \
            .filter(Restaurant.tables.any(Table.id.in_(
                [t.id for t in large_enough_table_ids_without_overlapping_reservations]))) \
            .all()
        
        return open_restaurants


    def _get_restriction_friendly_restaurants(self, session, eater_ids):
        # Get diets for eaters
        diets = session.query(Diet) \
            .join(Diet.eaters) \
            .filter(Eater.id.in_(eater_ids)) \
            .all()
        
        if len(diets) == 0:
            return session.query(Restaurant).all()

        # Subquery to count the number of matching diets for each restaurant
        # (We require all provided diets to be matched)
        matching_diets_subq = session.query(Restaurant.id, func.count(Diet.id).label('diet_count')) \
            .join(Restaurant.endorsements) \
            .filter(Diet.id.in_([diet.id for diet in diets])) \
            .group_by(Restaurant.id) \
            .having(func.count(Diet.id) == len(diets)) \
            .subquery()

        # Restaurants with matching diets and tables that can accommodate eaters
        # TODO optimization: just get ids
        restriction_friendly_restaurants = session.query(Restaurant) \
            .join(matching_diets_subq, Restaurant.id == matching_diets_subq.c.id) \
            .options(joinedload(Restaurant.tables), joinedload(Restaurant.endorsements)) \
            .filter(Restaurant.tables.any(Table.capacity >= len(eater_ids))) \
            .all()
        
        return restriction_friendly_restaurants
