from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import ReleaseFormORM

from .schemas import ReleaseFormCreateSchema, ReleaseFormUpdateSchema, ReleaseFormUpdatePartialSchema


async def get_release_forms(session: AsyncSession) ->[ReleaseFormORM]:
    stmt = select(ReleaseFormORM).order_by(ReleaseFormORM.id)
    result: Result = await session.execute(stmt)
    relese_froms = result.scalars().all()
    return list(relese_froms)

async def get_release_form(
        session: AsyncSession, 
        release_form_id: int
        ) -> ReleaseFormORM | None:
    return await session.get(ReleaseFormORM, release_form_id)

async def create_release_form(
        session: AsyncSession, 
        release_form_in: ReleaseFormCreateSchema
        ) -> ReleaseFormORM:
    release_form = ReleaseFormORM(**release_form_in.model_dump())
    session.add(release_form)
    await session.commit()
    #await session.refresh(release_form)
    return release_form

async def update_release_form(
        session: AsyncSession, 
        release_form: ReleaseFormORM, 
        release_form_update: ReleaseFormUpdateSchema | ReleaseFormUpdatePartialSchema,
        partial: bool = False,
        ) -> ReleaseFormORM:
    for name, value in release_form_update.model_dump(exclude_unset=partial).items():
        setattr(release_form, name, value)
    await session.commit()
    return release_form


async def delete_release_form(
        session: AsyncSession,
        release_form: ReleaseFormORM
) -> None:
    await session.delete(release_form)
    await session.commit()