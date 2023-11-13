import uuid

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import text
from .base import Base


class PharmacyORM(Base):
    __tablename__='pharmacy'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, server_default=text('gen_random_uuid()'))
    adress: Mapped[str]
    opening: Mapped[str]