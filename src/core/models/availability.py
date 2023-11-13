import uuid
from typing import TYPE_CHECKING


from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import text, Numeric, ForeignKey
from .base import Base

if TYPE_CHECKING:
    from .drug import DrugORM
    from .pharmacy import PharmacyORM

class AvailabilityORM(Base):
    __tablename__='availability'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, server_default=text('gen_random_uuid()'))
    quantity: Mapped[int]
    price: Mapped[float] = mapped_column(Numeric)

    drug_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('drug.id', ondelete='CASCADE'), 
        unique=True,
    )

    drug: Mapped[list['DrugORM']] = relationship(
        back_populates='availability',
        cascade='all, delete', 
        passive_deletes=True,
    )

    pharmacy: Mapped[list['PharmacyORM']] = relationship(
        back_populates='availability',
        secondary='available_in_pharmacy'
    )

    