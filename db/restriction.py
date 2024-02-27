from .db import db

restrictions = db.Table('restrictions',
    db.Column('diet_id', db.ForeignKey('diets.id'), primary_key=True),
    db.Column('eater_id', db.ForeignKey('eaters.id'), primary_key=True)
)