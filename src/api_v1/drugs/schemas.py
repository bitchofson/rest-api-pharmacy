import uuid
from core.models import Condition

from ..manufacturers.schemas import ManufacturerSchema
from ..release_forms.schemas import ReleaseFormSchema

from pydantic import BaseModel, ConfigDict

class DrugBaseSchema(BaseModel):
    name: str
    description: str
    leave_condition: Condition

class DrugSchema(DrugBaseSchema):
    model_config = ConfigDict(from_attributes=True)
    release_form: 'ReleaseFormSchema'
    manufacturer: 'ManufacturerSchema'
    id: uuid.UUID

class DrugCreateSchema(DrugBaseSchema):
    release_form_id: int
    manufacturer_id: uuid.UUID

class DrugUpdateSchema(DrugCreateSchema):
    pass

class DrugUpdatePartialSchema(DrugCreateSchema):
    name: str | None = None
    description: str | None = None
    leave_condition: Condition | None = None
    release_form_id: int | None = None
    manufacturer_id: uuid.UUID | None = None
