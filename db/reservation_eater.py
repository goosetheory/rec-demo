from .db import db

reservation_eaters = db.Table('reservation_eaters',
         db.Column('reservation_id', db.ForeignKey('reservations.id'), primary_key=True),
         db.Column('eater_id', db.ForeignKey('eaters.id'), primary_key=True)
)
