import pytest
from datetime import datetime


from db import db, Reservation, Restaurant, Eater, Diet, Table
from services import RestaurantService


class TestRestaurantService:
    @pytest.fixture
    def restaurant_service(self):
        return RestaurantService()

    @pytest.fixture()
    def large_group(self, db_session):
        eaters = [Eater(name=f'Eater {i}') for i in range(6)]
        db_session.add_all(eaters)
        db_session.commit()
        yield eaters
        for eater in eaters:
            db_session.delete(eater)

    @pytest.fixture()
    def vegan_restaurant(self, db_session, vegan_diet):
        restaurant = Restaurant(name='Vegan Restaurant')
        two_top_1 = Table(restaurant=restaurant, capacity=2)
        two_top_2 = Table(restaurant=restaurant, capacity=2)
        four_top = Table(restaurant=restaurant, capacity=4)
        restaurant.endorsements.append(vegan_diet)
        db_session.add(restaurant)
        db_session.commit()
        yield restaurant
        db_session.delete(restaurant)


    @pytest.fixture()
    def meat_restaurant(self, db_session):
        restaurant = Restaurant(name='Meat Restaurant')
        two_top_1 = Table(restaurant=restaurant, capacity=2)
        two_top_2 = Table(restaurant=restaurant, capacity=2)
        four_top = Table(restaurant=restaurant, capacity=4)
        db_session.add(restaurant)
        db_session.commit()
        yield restaurant
        db_session.delete(restaurant)

    @pytest.fixture()
    def restaurant_with_large_table(self, db_session):
        restaurant = Restaurant(name='Restaurant with Large Table')
        large_table = Table(restaurant=restaurant, capacity=6)
        db_session.add(restaurant)
        db_session.commit()
        yield restaurant
        db_session.delete(restaurant)


    @pytest.fixture()
    def vegan_diet(self, db_session):
        diet = Diet(restriction_name='Vegan', endorsement_name='Vegan Options')
        db_session.add(diet)
        db_session.commit()
        yield diet
        db_session.delete(diet)


    @pytest.fixture()
    def vegan_eater(self, db_session, vegan_diet):
        eater = Eater(name='Vegan Eater')
        eater.restrictions.append(vegan_diet)
        db_session.add(eater)
        db_session.commit()
        yield eater
        db_session.delete(eater)


    @pytest.fixture()
    def meat_eater(self, db_session):
        eater = Eater(name='Meat Eater')
        db_session.add(eater)
        db_session.commit()
        yield eater
        db_session.delete(eater)

    # @pytest.fixture()
    # def reservations_at_vegan_restaurant(self, db_session, vegan_restaurant, meat_eater):
    #     for table in vegan_restaurant.tables:
    #         reservation = Reservation(
    #             table=table,
    #             start_time=datetime.now(),
    #             eaters=[meat_eater]
    #         )
    #         db_session.add(reservation)
    #         db_session.commit()
    #     yield
    #     for table in vegan_restaurant.tables:
    #         for reservation in table.reservations:
    #             db_session.delete(reservation)


    def test_get_restaurants_for_meat_eater_no_reservations(
            self, restaurant_service, vegan_restaurant, meat_restaurant, meat_eater):
        # ACT
        result = restaurant_service.get_restaurants([meat_eater.id], datetime.now())

        # ASSERT
        assert len(result) == 2
        assert vegan_restaurant in result
        assert meat_restaurant in result


    def test_get_restaurants_for_vegan_eater_no_reservations(
            self, restaurant_service, vegan_restaurant, meat_restaurant, vegan_eater):
        # ACT
        result = restaurant_service.get_restaurants([vegan_eater.id], datetime.now())

        # ASSERT
        assert len(result) == 1
        assert vegan_restaurant in result

    def test_get_restaurants_for_meat_and_vegan_eater_no_reservations(
            self, restaurant_service, vegan_restaurant, meat_restaurant, vegan_eater, meat_eater):
        # ACT
        result = restaurant_service.get_restaurants([vegan_eater.id, meat_eater.id], datetime.now())

        # ASSERT
        assert len(result) == 1
        assert vegan_restaurant in result
    
    def test_get_restaurants_for_large_group_no_reservations(
            self, 
            restaurant_service,
            large_group,
            meat_restaurant,
            restaurant_with_large_table):
        # ACT
        result = restaurant_service.get_restaurants([eater.id for eater in large_group], datetime.now())
        
        # ASSERT
        assert len(result) == 1
        assert restaurant_with_large_table in result

    def test_get_restaurants_restaurant_is_booked(
            self,
            db_session,
            restaurant_service,
            vegan_restaurant,
            meat_restaurant,
            vegan_eater,
            meat_eater):
        # ARRANGE
        for table in vegan_restaurant.tables:
            reservation = Reservation(
                table=table,
                start_time=datetime.now(),
                eaters=[meat_eater]
            )
            db_session.add(reservation)
        db_session.commit()

        # ACT
        result = restaurant_service.get_restaurants([vegan_eater.id], datetime.now())

        # ASSERT
        assert len(result) == 0