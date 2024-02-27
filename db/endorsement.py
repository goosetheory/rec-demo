from .db import db

endorsements = db.Table('endorsements',
    db.Column('diet_id', db.ForeignKey('diets.id'), primary_key=True),
    db.Column('restaurant_id', db.ForeignKey('restaurants.id'), primary_key=True)
)
