import uuid
from datetime import datetime

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from .db import db

class Reservation(db.Model):
    __tablename__ = 'reservations'

    id: Mapped[uuid.uuid4] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    table_id: Mapped[uuid.uuid4] = mapped_column(ForeignKey('tables.id'), nullable=False)
    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    table = relationship('Table', back_populates='reservations')
    eaters = relationship('Eater', secondary='reservation_eaters', back_populates='reservations')

    def to_wire(self):
        return {
            'id': str(self.id),
            'table_id': str(self.table_id),
            'start_time': self.start_time.isoformat(),
            'eater_ids': [str(eater.id) for eater in self.eaters]
        }