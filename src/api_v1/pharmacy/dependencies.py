
from typing import Annotated
from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core import db_helper
from core.models import ReleaseFormORM
from . import crud

async def release_form_by_id(
    release_form_id: Annotated[int, Path], 
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
    ) -> ReleaseFormORM:
    release_form = await crud.get_release_form(session=session, release_form_id=release_form_id)
    if release_form is not None:
        return release_form
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Release form {release_form_id} not found!'
    )