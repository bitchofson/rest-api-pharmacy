from typing import TYPE_CHECKING


from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

if TYPE_CHECKING:
    from .drug import DrugORM

class ReleaseFormORM(Base):
    __tablename__='release_form'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement='auto')
    form: Mapped[str] = mapped_column(unique=True)

    drug: Mapped[list['DrugORM']] = relationship(
        back_populates='release_form',
        cascade='all, delete',
        passive_deletes=True,
    )