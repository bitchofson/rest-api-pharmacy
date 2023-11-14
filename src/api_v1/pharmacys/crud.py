import uuid

from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.pharmacy import PharmacyORM

from .schemas import PharmacyCreateSchema, PharmacyUpdateSchema, PharmacyUpdatePartialSchema


async def get_pharmacys(session: AsyncSession) -> list[PharmacyORM]:
    stmt = select(PharmacyORM).order_by(PharmacyORM.id)
    result: Result = await session.execute(stmt)
    result_orm = result.scalars().all()
    return list(result_orm)

async def get_pharmacy(
        session: AsyncSession,
        pharmacy_id: uuid.UUID
) -> PharmacyORM | None:
    return await session.get(PharmacyORM, pharmacy_id)

async def create_pharmacy(
        session: AsyncSession,
        pharmacy_in: PharmacyCreateSchema
) -> PharmacyORM:
    pharmacy = PharmacyORM(**pharmacy_in.model_dump())
    session.add(pharmacy)
    await session.commit()
    return pharmacy

async def update_pharmacy(
        session: AsyncSession,
        pharmacy: PharmacyORM,
        pharmacy_update: PharmacyUpdateSchema | PharmacyUpdatePartialSchema,
        partial: bool = False
) -> PharmacyORM:
    for name, value in pharmacy_update.model_dump(exclude_unset=partial).items():
        setattr(pharmacy, name, value)
    await session.commit()
    return pharmacy

async def delete_pharmacy(
        session: AsyncSession,
        pharmacy: PharmacyORM
) -> None:
    await session.delete(pharmacy)
    await session.commit();