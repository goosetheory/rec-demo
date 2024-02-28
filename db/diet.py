import uuid

from .db import db

from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

class Diet(db.Model):
    __tablename__ = 'diets'

    id: Mapped[uuid.uuid4] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    restriction_name: Mapped[str] = mapped_column(Text, nullable=False)
    endorsement_name: Mapped[str] = mapped_column(Text, nullable=False)

    eaters = relationship('Eater', secondary='restrictions', back_populates='restrictions')
    restaurants = relationship('Restaurant', secondary='endorsements', back_populates='endorsements')