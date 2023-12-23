from fastapi import APIRouter, status, Depends, Query
from fastapi_pagination import Page, paginate
from sqlalchemy.ext.asyncio import AsyncSession

from core import db_helper

from . import crud
from .schemas import ReleaseFormSchema, ReleaseFormCreateSchema, ReleaseFormUpdateSchema, ReleaseFormUpdatePartialSchema
from ..dependencies import release_form_by_id

router = APIRouter(tags=['Release Forms'])

@router.get('/', response_model=Page[ReleaseFormSchema])
async def get_release_forms(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    filter: str = Query(None, alias="filter")
    ):
    return paginate(await crud.get_release_forms(session=session, filter=filter))

@router.post('/', response_model=ReleaseFormSchema,
             status_code=status.HTTP_201_CREATED)
async def create_release_form(
    release_form_in: ReleaseFormCreateSchema,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
    ):
    return await crud.create_release_form(session=session, release_form_in=release_form_in)

@router.get('/{release_form_id}', response_model=ReleaseFormSchema)
async def get_release_form(
    release_form: ReleaseFormSchema = Depends(release_form_by_id)
    ):
    return release_form

@router.put('/{release_form_id}')
async def update_release_form(
    release_form_update: ReleaseFormUpdateSchema,
    release_form: ReleaseFormSchema = Depends(release_form_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.update_release_form(
        session=session,
        release_form=release_form,
        release_form_update=release_form_update
    )

@router.patch('/{release_form_id}')
async def update_release_form_partial(
    release_form_update: ReleaseFormUpdatePartialSchema,
    release_form: ReleaseFormSchema = Depends(release_form_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.update_release_form(
        session=session,
        release_form=release_form,
        release_form_update=release_form_update,
        partial=True
    )

@router.delete('/{release_form_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_release_form(
    release_form: ReleaseFormSchema = Depends(release_form_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
) -> None:
    await crud.delete_release_form(session=session, release_form=release_form)

