import uuid

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
        # Hardcoded UUIDs for eaters
        michael = Eater(id=uuid.UUID('cfd13932-bb49-4ebf-b6a3-00be65e0fe2e'), name='Michael', restrictions=[vegetarian_diet])
        george_michael = Eater(id=uuid.UUID('7b9ccf03-e115-4c93-b81d-2fe73c4d5a34'), name='George Michael', restrictions=[vegetarian_diet, gluten_free_diet])
        lucile = Eater(id=uuid.UUID('b4bc68d8-ebbd-45f9-9ed7-1c1513ee8559'), name='Lucile', restrictions=[gluten_free_diet])
        gob = Eater(id=uuid.UUID('37096eb3-d346-4606-8f96-1fee2e07d112'), name='Gob', restrictions=[paleo_diet])
        tobias = Eater(id=uuid.UUID('aec0c7a7-4156-4c79-8f9e-1f4592ec0cee'), name='Tobias')
        maeby = Eater(id=uuid.UUID('7d8f2ee1-1643-41cf-a065-a71435f7fd2f'), name='Maeby', restrictions=[vegan_diet])

        session.add_all([michael, george_michael, lucile, gob, tobias, maeby])

        print('Seeding restaurants...')
        # Hardcoded UUIDs for restaurants
        lardo = Restaurant(id=uuid.UUID('200e0fb3-4d15-4b0f-82f4-c3ec49df80ef'), name='Lardo', endorsements=[gluten_free_diet])
        panaderia_rosetta = Restaurant(id=uuid.UUID('115ce652-5aa7-4e83-bd6a-c6d9f039e514'), name='Panadería Rosetta', endorsements=[vegetarian_diet, gluten_free_diet])
        tetetlan = Restaurant(id=uuid.UUID('cfb233ad-2c23-4eb9-b41e-f2cce1447e79'), name='Tetetlán', endorsements=[paleo_diet, gluten_free_diet])
        falling_piano = Restaurant(id=uuid.UUID('ba63f110-3fd4-46e2-b72a-b0f55df729d2'), name='Falling Piano Brewing Co')
        # Note: anywhere that has a vegan endorsement is also vegetarian-friendly
        utopia = Restaurant(id=uuid.UUID('c08baffa-71a1-4b20-ba75-af2849a9974d'), name='u.to.pi.a', endorsements=[vegan_diet, vegetarian_diet])

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
        session.query(Reservation).delete()
        session.query(Table).delete()
        session.query(Eater).delete()
        session.query(Restaurant).delete()
        session.query(Diet).delete()
        print('Database emptied.')