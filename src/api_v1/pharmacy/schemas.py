from pydantic import BaseModel, ConfigDict


class ReleaseFormBaseSchema(BaseModel):
    form: str

class ReleaseFormCreateSchema(ReleaseFormBaseSchema):
    pass

class ReleaseFormUpdateSchema(ReleaseFormCreateSchema):
    pass

class ReleaseFormUpdatePartialSchema(ReleaseFormCreateSchema):
    form: str | None = None

class ReleaseFormSchema(ReleaseFormBaseSchema):
    model_config = ConfigDict(from_attributes=True)
    id: int