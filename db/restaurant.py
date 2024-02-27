import uuid

from .db import db

from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

class Restaurant(db.Model):
    __tablename__ = 'restaurants'

    id: Mapped[uuid.uuid4] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(Text, nullable=False)

    tables = relationship('Table', back_populates='restaurant')
    endorsements = relationship('Diet', secondary='endorsements', back_populates='restaurants')