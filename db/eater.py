import uuid

from .db import db

from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

class Eater(db.Model):
    __tablename__ = 'eaters'

    id: Mapped[uuid.uuid4] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(Text, nullable=False)

    reservations = relationship('Reservation', secondary='reservation_eaters', back_populates='eaters')
    restrictions = relationship('Diet', secondary='restrictions', back_populates='eaters')
