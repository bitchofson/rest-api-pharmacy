import uuid
from fastapi import APIRouter, status, Depends, Query
from fastapi_pagination import Page, paginate
from sqlalchemy.ext.asyncio import AsyncSession

from core import db_helper

from . import crud
from ..availability_pharmacys_schemes import (
    AvailabilitySchema, 
    AvailabilityCreateSchema, 
    AvailabilityUpdateSchema, 
    AvailabilityUpdatePartialSchema,
    AvailabilityInPharmacySchema,
    PharmacySchema
)
from ..dependencies import availability_by_id, pharmacy_by_id

router = APIRouter(tags=['Availabilitys'])

@router.get('/', response_model=Page[AvailabilityInPharmacySchema])
async def get_availabilitys(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    filter: str = Query(None, alias="filter")
):
    return paginate(await crud.get_availabilitys(session=session, filter=filter))
    
@router.get('/{availability_id}', response_model=AvailabilityInPharmacySchema)
async def get_availabilitys(
    availability: AvailabilityInPharmacySchema = Depends(availability_by_id)
):
    return availability

@router.post('/', response_model=AvailabilityCreateSchema,
             status_code=status.HTTP_201_CREATED)
async def create_availability(
    availability_in: AvailabilityCreateSchema,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.create_availability(session=session, availability_in=availability_in)


@router.put('/{availability_id}', response_model=AvailabilityUpdateSchema)
async def update_availability(
    availability_update: AvailabilityUpdateSchema,
    availability: AvailabilitySchema = Depends(availability_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.update_availability(
        session=session,
        availability=availability,
        availability_update=availability_update
    )

@router.patch('/{availability_id}', response_model=AvailabilityUpdatePartialSchema)
async def update_availability_partial(
    availability_update: AvailabilityUpdatePartialSchema,
    availability: AvailabilitySchema = Depends(availability_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.update_availability(
        session=session,
        availability=availability,
        availability_update=availability_update,
        partial=True
    )

@router.delete('/{availability_id}', 
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_availability(
    availability: AvailabilitySchema = Depends(availability_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    await crud.delete_availability(session=session, availability=availability)


@router.post('/{availability_id}/pharmacy/{pharmacy_id}', 
             response_model=AvailabilityInPharmacySchema,
             status_code=status.HTTP_201_CREATED)
async def add_pharmacy_in_availability(
    availability_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    pharmacy: PharmacySchema = Depends(pharmacy_by_id)
):
    return await crud.add_pharmacy_in_available(
        availability_id=availability_id,
        session=session, 
        pharmacy=pharmacy)

@router.delete('/{availability_id}/pharmacy/{pharmacy_id}', 
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_pharmacy_from_availability(
    availability_id: uuid.UUID,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    pharmacy: PharmacySchema = Depends(pharmacy_by_id)
):
    await crud.delete_pharmacy_from_available(
        availability_id=availability_id,
        session=session, 
        pharmacy=pharmacy)
