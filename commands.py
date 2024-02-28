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
        session.query(Eater).delete()
        session.query(Restaurant).delete()
        session.query(Table).delete()
        session.query(Diet).delete()
        session.query(Reservation).delete()
        session.query(reservation_eaters).delete()
        session.query(restrictions).delete()
        session.query(endorsements).delete()