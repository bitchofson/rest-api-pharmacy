from fastapi import APIRouter, status, Depends
from fastapi_pagination import Page, paginate
from sqlalchemy.ext.asyncio import AsyncSession

from core import db_helper

from . import crud
from .schemas import DrugSchema, DrugCreateSchema, DrugUpdateSchema, DrugUpdatePartialSchema
from ..dependencies import drug_by_id

router = APIRouter(tags=['Drugs'])

@router.get('/', response_model=Page[DrugSchema])
async def get_drugs(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return paginate(await crud.get_drugs(session=session))

@router.get('/{drug_id}', response_model=DrugSchema)
async def get_drug(
    drug: DrugSchema = Depends(drug_by_id)
):
    return drug

@router.post('/', response_model=DrugCreateSchema,
             status_code=status.HTTP_201_CREATED)
async def create_drug(
    drug: DrugCreateSchema,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_drug(session=session, drug_in=drug)

@router.put('/{drug_id}', response_model=DrugUpdateSchema)
async def update_drug(
    drug_update: DrugUpdateSchema,
    drug: DrugSchema = Depends(drug_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.update_drug(
        session=session,
        drug=drug,
        drug_update=drug_update
    )

@router.patch('/{drug_id}', response_model=DrugUpdatePartialSchema)
async def update_drug_partial(
    drug_update: DrugUpdatePartialSchema,
    drug: DrugSchema = Depends(drug_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.update_drug(
        session=session,
        drug=drug,
        drug_update=drug_update,
        partial=True
    )

@router.delete('/{drug_id}', 
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_drug(
    drug: DrugSchema = Depends(drug_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    await crud.delete_drug(session=session, drug=drug)