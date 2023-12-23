import uuid
from fastapi import APIRouter, status, Depends, Query
from fastapi_pagination import Page, paginate
from sqlalchemy.ext.asyncio import AsyncSession

from core import db_helper

from . import crud
from ..availability_pharmacys_schemes import (
    PharmacySchema,
    PharmacyCreateSchema, 
    PharmacyUpdateSchema, 
    PharmacyUpdatePartialSchema,
    PharmacyWithAvailabilitySchema,
    AvailabilitySchema
)
from ..dependencies import pharmacy_by_id, availability_by_id

router = APIRouter(tags=['Pharmacys'])

@router.get('/', response_model=Page[PharmacyWithAvailabilitySchema])
async def get_pharmacys(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    filter: str = Query(None, alias="filter")
):
    return paginate(await crud.get_pharmacys(session=session, filter=filter))

@router.get('/{pharmacy_id}', response_model=PharmacyWithAvailabilitySchema)
async def get_pharmacy(
    pharmacy: PharmacyWithAvailabilitySchema = Depends(pharmacy_by_id)
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

@router.post('/{pharmacy_id}/availability/{availability_id}', 
             response_model=PharmacyWithAvailabilitySchema,
             status_code=status.HTTP_201_CREATED)
async def add_availability_in_pharmacy(
    pharmacy_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    availability: AvailabilitySchema = Depends(availability_by_id)
):
    return await crud.add_available_in_pharmacy(
        pharmacy_id=pharmacy_id,
        session=session,
        availability=availability
    )

@router.delete('/{pharmacy_id}/availability/{availability_id}', 
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_availability_from_pharmacy(
    pharmacy_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    availability: AvailabilitySchema = Depends(availability_by_id)
):
    await crud.delete_pharmacy_from_available(
        pharmacy_id=pharmacy_id,
        session=session,
        availability=availability
    )