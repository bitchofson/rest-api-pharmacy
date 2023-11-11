import enum

from sqlalchemy.orm import DeclarativeBase

class Condition(enum.Enum):
    reception_yes = 'По рецепту'
    reception_no = 'Без рецепта'
    
class Base(DeclarativeBase):
    pass