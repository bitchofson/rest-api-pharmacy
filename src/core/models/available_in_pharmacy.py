import uuid

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from .base import Base


class AvailableInPharmacyORM(Base):
    __tablename__='available_in_pharmacy'

    pharmacy_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('pharmacy.id'),
        primary_key=True, )
    
    availability_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('availability.id'),
        primary_key=True, )