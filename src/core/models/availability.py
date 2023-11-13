import uuid

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import text, Numeric, ForeignKey
from .base import Base


class AvailabilityORM(Base):
    __tablename__='availability'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, server_default=text('gen_random_uuid()'))
    quantity: Mapped[int]
    price: Mapped[float] = mapped_column(Numeric)

    drug_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('drug.id', ondelete='CASCADE'), 
        unique=True,
    )