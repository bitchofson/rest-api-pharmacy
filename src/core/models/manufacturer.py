import uuid

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import text
from .base import Base


class ManufacturerORM(Base):
    __tablename__='manufacturer'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, server_default=text('gen_random_uuid()'))
    name: Mapped[str] = mapped_column(unique=True)