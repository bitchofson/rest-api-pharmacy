from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core import db_helper

from . import crud
from .schemas import AvailabilitySchema, AvailabilityCreateSchema, AvailabilityUpdateSchema, AvailabilityUpdatePartialSchema
from ..dependencies import availability_by_id

router = APIRouter(tags=['Availabilitys'])

@router.get('/', response_model=list[AvailabilitySchema])
async def get_availabilitys(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.get_availabilitys(session=session)

@router.get('/{availability_id}', response_model=AvailabilitySchema)
async def get_availabilitys(
    availability: AvailabilitySchema = Depends(availability_by_id)
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
