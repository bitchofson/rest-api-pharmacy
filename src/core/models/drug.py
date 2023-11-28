import uuid
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import text, Text, ForeignKey
from .base import Base, Condition

if TYPE_CHECKING:
    from .release_form import ReleaseFormORM
    from .manufacturer import ManufacturerORM
    from .availability import AvailabilityORM

class DrugORM(Base):
    __tablename__='drug'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, server_default=text('gen_random_uuid()'))
    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column(Text)
    leave_condition: Mapped[Condition]

    release_form_id: Mapped[int] = mapped_column(
        ForeignKey('release_form.id', ondelete='CASCADE')
    )
    manufacturer_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('manufacturer.id', ondelete='CASCADE')
    )

    release_form: Mapped['ReleaseFormORM'] = relationship(back_populates='drug')
    manufacturer: Mapped['ManufacturerORM'] = relationship(back_populates='drug')
    availability: Mapped['AvailabilityORM'] = relationship(
        back_populates='drug',
        cascade='all, delete',
        passive_deletes=True,)