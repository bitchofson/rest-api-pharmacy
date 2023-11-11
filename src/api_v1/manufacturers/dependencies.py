import uuid

from typing import Annotated
from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core import db_helper
from core.models import ManufacturerORM
from . import crud

async def manufacturer_by_id(
    manufacturer_id: Annotated[uuid.UUID, Path], 
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
    ) -> ManufacturerORM:
    manufacturer = await crud.get_manufacturer(session=session, manufacturer_id=manufacturer_id)
    if manufacturer is not None:
        return manufacturer
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Manufacturer {manufacturer_id} not found!'
    )