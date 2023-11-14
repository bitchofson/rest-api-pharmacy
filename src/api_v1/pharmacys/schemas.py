import uuid

from pydantic import BaseModel, ConfigDict

class PharmacyBaseSchema(BaseModel):
    name: str
    adress: str
    opening: str

class PharmacySchema(PharmacyBaseSchema):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID

class PharmacyCreateSchema(PharmacyBaseSchema):
    pass

class PharmacyUpdateSchema(PharmacyCreateSchema):
    pass

class PharmacyUpdatePartialSchema(PharmacyCreateSchema):
    name: str | None = None
    adress: str | None = None
    opening: str | None = None