import uuid
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import text
from .base import Base

if TYPE_CHECKING:
    from .availability import AvailabilityORM

class PharmacyORM(Base):
    __tablename__='pharmacy'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, server_default=text('gen_random_uuid()'))
    adress: Mapped[str]
    opening: Mapped[str]

    availability: Mapped[list['AvailabilityORM']] = relationship(
        back_populates='pharmacy',
        secondary='available_in_pharmacy'
    )