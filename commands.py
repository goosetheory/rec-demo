from flask import Blueprint
from flask.cli import with_appcontext

from db import session_scope, Eater, Restaurant, Table, Diet, Reservation, \
    reservation_eaters, restrictions, endorsements

commands = Blueprint('commands', __name__)

@commands.cli.command('seed-db')
@with_appcontext
def seed_db():
    with session_scope() as session:
        print('Seeding diets...')
        vegetarian_diet = Diet(restriction_name='Vegetarian', endorsement_name='Vegetarian-Friendly')
        vegan_diet = Diet(restriction_name='Vegan', endorsement_name='Vegan-Friendly')
        gluten_free_diet = Diet(restriction_name='Gluten-Free', endorsement_name='Gluten Free Options')
        paleo_diet = Diet(restriction_name='Paleo', endorsement_name='Paleo-Friendly')
        
        session.add_all([vegetarian_diet, vegan_diet, gluten_free_diet, paleo_diet])

        print('Seeding eaters...')
        michael = Eater(name='Michael', restrictions=[vegetarian_diet])
        george_michael = Eater(name='George Michael', restrictions=[vegetarian_diet, gluten_free_diet])
        lucile = Eater(name='Lucile', restrictions=[gluten_free_diet])
        gob = Eater(name='Gob', restrictions=[paleo_diet])
        tobias = Eater(name='Tobias')
        maeby = Eater(name='Maeby', restrictions=[vegan_diet])

        session.add_all([michael, george_michael, lucile, gob, tobias, maeby])

        print('Seeding restaurants...')
        lardo = Restaurant(name='Lardo', endorsements=[gluten_free_diet])
        panaderia_rosetta = Restaurant(name='Panadería Rosetta', endorsements=[vegetarian_diet, gluten_free_diet])
        tetetlan = Restaurant(name='Tetetlán', endorsements=[paleo_diet, gluten_free_diet])
        falling_piano = Restaurant(name='Falling Piano Brewing Co')
        # Note: anywhere that has a vegan diet is also vegetarian-friendly
        utopia = Restaurant(name='u.to.pi.a', endorsements=[vegan_diet, vegetarian_diet])

        session.add_all([lardo, panaderia_rosetta, tetetlan, falling_piano, utopia])

        print('Seeding tables...')
        tables = []
        tables.extend(_create_tables(lardo, capacity=2, number=4))
        tables.extend(_create_tables(lardo, capacity=4, number=2))
        tables.extend(_create_tables(lardo, capacity=6, number=1))

        tables.extend(_create_tables(panaderia_rosetta, capacity=2, number=3))
        tables.extend(_create_tables(panaderia_rosetta, capacity=4, number=2))
        
        tables.extend(_create_tables(tetetlan, capacity=2, number=4))
        tables.extend(_create_tables(tetetlan, capacity=4, number=2))
        tables.extend(_create_tables(tetetlan, capacity=6, number=1))
        
        tables.extend(_create_tables(falling_piano, capacity=2, number=5))
        tables.extend(_create_tables(falling_piano, capacity=4, number=5))
        tables.extend(_create_tables(falling_piano, capacity=6, number=5))
        
        tables.extend(_create_tables(utopia, capacity=2, number=2))

        session.add_all(tables)

        print('Database seeding complete.')


def _create_tables(restaurant, capacity, number):
    tables = [Table(restaurant=restaurant, capacity=capacity) for _ in range(number)]
    return tables



@commands.cli.command('empty-db')
@with_appcontext
def empty_db():
    with session_scope() as session:
        # Note to Rec: I'd need a compelling reason to keep this code in past
        # early testing. It would probably be accompanied by a comment like:
        # TODO(<link to ticket>): Remove this command before setting up prod env

        print('Deleting all DB data. Running in prod is gently cautioned against.')
        confirmation = input('Type "yes" to confirm: ')
        if confirmation != 'yes':
            print('Aborting...')
            return

        print('Emptying database...')
        session.query(reservation_eaters).delete()
        session.query(restrictions).delete()
        session.query(endorsements).delete()
        session.query(Eater).delete()
        session.query(Restaurant).delete()
        session.query(Table).delete()
        session.query(Diet).delete()
        session.query(Reservation).delete()
        print('Database emptied.')