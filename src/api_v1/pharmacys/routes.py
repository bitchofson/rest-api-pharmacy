from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core import db_helper

from . import crud
from .schemas import PharmacySchema, PharmacyCreateSchema, PharmacyUpdateSchema, PharmacyUpdatePartialSchema
from ..dependencies import pharmacy_by_id

router = APIRouter(tags=['Pharmacys'])

@router.get('/', response_model=list[PharmacySchema])
async def get_pharmacys(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.get_pharmacys(session=session)

@router.get('/{pharmacy_id}', response_model=PharmacySchema)
async def get_pharmacy(
    pharmacy: PharmacySchema = Depends(pharmacy_by_id)
):
    return pharmacy

@router.post('/', response_model=PharmacyCreateSchema,
             status_code=status.HTTP_201_CREATED)
async def create_pharmacy(
    pharmacy_in: PharmacyCreateSchema,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.create_pharmacy(pharmacy_in=pharmacy_in, session=session)

@router.put('/{pharmacy_id}', response_model=PharmacyUpdateSchema)
async def update_drug(
    pharmacy_update: PharmacyUpdateSchema,
    pharmacy: PharmacySchema = Depends(pharmacy_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.update_pharmacy(
        session=session,
        pharmacy=pharmacy,
        pharmacy_update=pharmacy_update
    )

@router.patch('/{pharmacy_id}', response_model=PharmacyUpdatePartialSchema)
async def update_pharmacy(
    pharmacy_update: PharmacyUpdatePartialSchema,
    pharmacy: PharmacySchema = Depends(pharmacy_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.update_pharmacy(
        session=session,
        pharmacy=pharmacy,
        pharmacy_update=pharmacy_update,
        partial=True
    )

@router.delete('/{pharmacy_id}', 
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_pharmacy(
    pharmacy: PharmacySchema = Depends(pharmacy_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    await crud.delete_pharmacy(session=session, pharmacy=pharmacy)