import uuid

from sqlalchemy import select, or_, text
from sqlalchemy.orm import selectinload
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from core.models.drug import DrugORM

from .schemas import DrugCreateSchema, DrugUpdateSchema, DrugUpdatePartialSchema

async def get_drugs(session: AsyncSession, filter: str) -> list[DrugORM]:
    
    stmt = (
        select(DrugORM)
        .options(
            selectinload(DrugORM.release_form),
            selectinload(DrugORM.manufacturer)
            )
    )
    if filter is not None and filter != 'null':
        criteria = dict(x.split("*") for x in filter.split('-'))
        print(criteria)
        criteria_list = []

        for attr, value in criteria.items():
                search = '%{}%'.format(value)
                criteria_list.append(getattr(DrugORM, attr).like(search))
        
        stmt = stmt.filter(or_(*criteria_list))

    result: Result = await session.execute(stmt)
    result_orm = result.scalars().all()
    return list(result_orm)

async def get_count_recepctions(session: AsyncSession) -> list[DrugORM]:

    result: Result = await session.execute(text('SELECT leave_condition, COUNT(*) AS count FROM drug GROUP BY leave_condition;'))
    list = result.all()
    converted_list = []
    for item in list:
        converted_list.append({item[0]: item[1]})
    return converted_list

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