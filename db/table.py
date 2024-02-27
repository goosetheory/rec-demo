import uuid

from .db import db

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

class Table(db.Model):
    __tablename__ = 'tables'

    id: Mapped[uuid.uuid4] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    restaurant_id: Mapped[uuid.uuid4] = mapped_column(ForeignKey('restaurants.id'), nullable=False)
    capacity: Mapped[int] = mapped_column(Text, nullable=False)

    restaurant = relationship('Restaurant', back_populates='tables')
    reservations = relationship('Reservation', back_populates='table')