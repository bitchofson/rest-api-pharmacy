import uuid

from pydantic import BaseModel, ConfigDict


class ManufacturerBaseSchema(BaseModel):
    name: str
    adress: str

class ManufacturerSchema(ManufacturerBaseSchema):
    id: uuid.UUID
    model_config = ConfigDict(from_attributes=True)

class ManufacturerCreateSchema(ManufacturerBaseSchema):
    pass

class ManufacturerUpdateSchema(ManufacturerCreateSchema):
    pass

class ManufacturerUpdatePartialSchema(ManufacturerCreateSchema):
    name: str | None = None
    adress: str | None = None