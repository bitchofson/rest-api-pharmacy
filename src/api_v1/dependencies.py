import uuid

from typing import Annotated
from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core import db_helper
from core.models import ManufacturerORM, ReleaseFormORM, DrugORM

from .release_forms import crud as crud_release_form
from .manufacturers import crud as crud_manufacturer
from .drugs import crud as crud_drug

async def manufacturer_by_id(
    manufacturer_id: Annotated[uuid.UUID, Path], 
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
    ) -> ManufacturerORM:
    manufacturer = await crud_manufacturer.get_manufacturer(session=session, manufacturer_id=manufacturer_id)
    if manufacturer is not None:
        return manufacturer
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Manufacturer with {manufacturer_id} id not found!'
    )

async def release_form_by_id(
    release_form_id: Annotated[int, Path], 
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
    ) -> ReleaseFormORM:
    release_form = await crud_release_form.get_release_form(session=session, release_form_id=release_form_id)
    if release_form is not None:
        return release_form
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Release form with {release_form_id} id not found!'
    )

async def drug_by_id(
        drug_id: Annotated[uuid.UUID, Path],
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
) -> DrugORM:
    drug = await crud_drug.get_drug(session=session, drug_id=drug_id)
    if drug is not None:
        return drug
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Drug with {drug_id} id not found!'
    )