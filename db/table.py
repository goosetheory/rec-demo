import uuid

from .db import db

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

# Note to Rec: Tables could also have been represented in a more "flat" way.
# This table would instead be called "capacities", perhaps, and would
# store a restaurant id, a capacity, and a number of tables at that restaurant
# with that capacity. But this allows for tables to have attributes
# other than capacity in the future, e.g. window seating, booth vs chairs, etc.
class Table(db.Model):
    __tablename__ = 'tables'

    id: Mapped[uuid.uuid4] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    restaurant_id: Mapped[uuid.uuid4] = mapped_column(ForeignKey('restaurants.id'), nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)

    restaurant = relationship('Restaurant', back_populates='tables', uselist=False)
    reservations = relationship('Reservation', back_populates='table')
