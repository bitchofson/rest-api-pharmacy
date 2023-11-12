import uuid
from typing import TYPE_CHECKING


from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import text
from .base import Base

if TYPE_CHECKING:
    from .drug import DrugORM

class ManufacturerORM(Base):
    __tablename__='manufacturer'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, server_default=text('gen_random_uuid()'))
    name: Mapped[str] = mapped_column(unique=True)

    drug: Mapped[list['DrugORM']] = relationship(
        back_populates='manufacturer', 
        cascade='all, delete', 
        passive_deletes=True,
    )