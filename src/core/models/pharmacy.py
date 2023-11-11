from sqlalchemy.orm import Mapped, mapped_column
from .base import Base

class ReleaseFormORM(Base):
    __tablename__='release_form'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement='auto')
    form: Mapped[str] = mapped_column(unique=True)