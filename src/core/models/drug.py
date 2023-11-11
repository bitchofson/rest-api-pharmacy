import uuid

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import text, Text, ForeignKey
from .base import Base, Condition


class DrugORM(Base):
    __tablename__='drug'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, server_default=text('gen_random_uuid()'))
    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column(Text)
    leave_condition: Mapped[Condition]

    release_form_id: Mapped[int] = mapped_column(
        ForeignKey('release_form.id', ondelete='SET NULL')
    )
    manufacturer_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('manufacturer.id', ondelete='SET NULL')
    )