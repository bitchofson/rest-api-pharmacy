from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core import db_helper

from . import crud
from .schemas import ManufacturerSchema, ManufacturerCreateSchema, ManufacturerUpdateSchema, ManufacturerUpdatePartialSchema
from ..dependencies import manufacturer_by_id

router = APIRouter(tags=['Manufacturers'])

@router.get('/', response_model=list[ManufacturerSchema])
async def get_manufacturers(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.get_manufacturers(session=session)

@router.post('/', response_model=ManufacturerSchema,
             status_code=status.HTTP_201_CREATED)
async def create_manufacturer(
    manufacturer_in: ManufacturerCreateSchema,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.create_manufacturer(session=session, manufacturer_in=manufacturer_in)


@router.get('/{manufacturer_id}', response_model=ManufacturerSchema)
async def get_manufacturer(
    release_form: ManufacturerSchema = Depends(manufacturer_by_id)
):
    return release_form

@router.put('/{manufacturer_id}')
async def update_manufacturer(
    manufacturer_update: ManufacturerUpdateSchema,
    manufacturer: ManufacturerSchema = Depends(manufacturer_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.update_manufacturer(
        session=session,
        manufacturer=manufacturer,
        manufacturer_update=manufacturer_update 
    )

@router.patch('/{manufacturer_id}')
async def update_manufacturer_partial(
    manufacturer_update: ManufacturerUpdatePartialSchema,
    manufacturer: ManufacturerSchema = Depends(manufacturer_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.update_manufacturer(
        session=session,
        manufacturer=manufacturer,
        manufacturer_update=manufacturer_update,
        partial=True
    )

@router.delete('/{manufacturer_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_manufacturer(
    manufacturer: ManufacturerSchema = Depends(manufacturer_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
) -> None:
    await crud.delete_manufacturer(session=session, manufacturer=manufacturer)