import uuid

from .drugs.schemas import DrugSchema
from pydantic import BaseModel, ConfigDict


class AvailabilityBaseSchema(BaseModel):
    quantity:int
    price: float


class AvailabilitySchema(AvailabilityBaseSchema):
    id: uuid.UUID
    model_config = ConfigDict(from_attributes=True)
    drug: 'DrugSchema'

class AvailabilityCreateSchema(AvailabilityBaseSchema):
    drug_id: uuid.UUID

class AvailabilityUpdateSchema(AvailabilityCreateSchema):
    pass

class AvailabilityUpdatePartialSchema(AvailabilityCreateSchema):
    quantity: int | None = None
    price: float | None = None
    drug_id: uuid.UUID | None = None

    

class PharmacyBaseSchema(BaseModel):
    name: str
    adress: str
    opening: str

class PharmacySchema(PharmacyBaseSchema):
    id: uuid.UUID
    model_config = ConfigDict(from_attributes=True)


class PharmacyCreateSchema(PharmacyBaseSchema):
    pass

class PharmacyUpdateSchema(PharmacyCreateSchema):
    pass

class PharmacyUpdatePartialSchema(PharmacyCreateSchema):
    name: str | None = None
    adress: str | None = None
    opening: str | None = None

class PharmacyWithAvailabilitySchema(PharmacySchema):
    availability: list['AvailabilitySchema']

class AvailabilityInPharmacySchema(AvailabilitySchema):
    pharmacy: list['PharmacySchema']