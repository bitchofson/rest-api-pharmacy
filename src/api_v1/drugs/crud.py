import uuid

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.drug import DrugORM

from .schemas import DrugCreateSchema, DrugUpdateSchema, DrugUpdatePartialSchema

async def get_drugs(session: AsyncSession) -> list[DrugORM]:
    stmt = (
        select(DrugORM)
        .options(
            selectinload(DrugORM.release_form),
            selectinload(DrugORM.manufacturer)
            )
    )

    result: Result = await session.execute(stmt)
    result_orm = result.scalars().all()
    return list(result_orm)

async def get_drug(
        session: AsyncSession,
        drug_id: uuid.UUID
) -> DrugORM | None:
    stmt = (
        select(DrugORM)
        .options(
            selectinload(DrugORM.release_form),
            selectinload(DrugORM.manufacturer)
        ).where(DrugORM.id == drug_id)
    )

    result: Result = await session.execute(stmt)
    result_orm = result.scalar_one_or_none()
    return result_orm

async def create_drug(
        session: AsyncSession,
        drug_in: DrugCreateSchema
) -> DrugORM:
    drug = DrugORM(**drug_in.model_dump())
    session.add(drug)
    await session.commit()
    return drug

async def update_drug(
        session: AsyncSession,
        drug: DrugORM,
        drug_update: DrugUpdateSchema | DrugUpdatePartialSchema,
        partial: bool = False
) -> DrugORM:
    for name, value in drug_update.model_dump(exclude_unset=partial).items():
        setattr(drug, name, value)
    await session.commit()
    return drug

async def delete_drug(
        session: AsyncSession,
        drug: DrugORM
) -> None:
    await session.delete(drug)
    await session.commit()