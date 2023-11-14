import uuid
from pydantic import BaseModel, ConfigDict
from ..availabilitys.schemas import AvailabilitySchema

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

class PharmacyWithvAvailabilitySchema(PharmacySchema):
    availability: list['AvailabilitySchema']