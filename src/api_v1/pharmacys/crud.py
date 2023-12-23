import uuid

from sqlalchemy import select, or_
from sqlalchemy.orm import selectinload
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.pharmacy import PharmacyORM
from core.models.availability import AvailabilityORM
from core.models.drug import DrugORM

from ..availability_pharmacys_schemes import (
    PharmacyCreateSchema, 
    PharmacyUpdateSchema, 
    PharmacyUpdatePartialSchema
)

async def get_pharmacys(session: AsyncSession, filter: str) -> list[PharmacyORM]:
    stmt = (
        select(PharmacyORM)
            .options(
                selectinload(PharmacyORM.availability).options(
                    selectinload(AvailabilityORM.drug).options(
                        selectinload(DrugORM.release_form),
                        selectinload(DrugORM.manufacturer)
                    )
                )
            )
    )

    if filter is not None and filter != 'null':
        criteria = dict(x.split("*") for x in filter.split('-'))
        print(criteria)
        criteria_list = []

        for attr, value in criteria.items():
                search = '%{}%'.format(value)
                criteria_list.append(getattr(PharmacyORM, attr).like(search))
        
        stmt = stmt.filter(or_(*criteria_list))

    result: Result = await session.execute(stmt)
    result_orm = result.scalars().all()
    return list(result_orm)

async def get_pharmacy(
        session: AsyncSession,
        pharmacy_id: uuid.UUID
) -> PharmacyORM | None:
    stmt = (
        select(PharmacyORM)
            .options(
                selectinload(PharmacyORM.availability).options(
                    selectinload(AvailabilityORM.drug).options(
                        selectinload(DrugORM.release_form),
                        selectinload(DrugORM.manufacturer)
                    )
                )
            ).where(PharmacyORM.id == pharmacy_id)
    )

    result: Result = await session.execute(stmt)
    result_orm = result.scalar_one_or_none()
    return result_orm

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

async def add_available_in_pharmacy(
        pharmacy_id: uuid.UUID,
        session: AsyncSession,
        availability: AvailabilityORM,
):
    pharmacy = await get_pharmacy(session, pharmacy_id=pharmacy_id)
    pharmacy.availability.append(availability)
    await session.commit()
    return pharmacy

async def delete_pharmacy_from_available(
        pharmacy_id: uuid.UUID,
        session: AsyncSession,
        availability: AvailabilityORM,
):
    pharmacy = await get_pharmacy(session, pharmacy_id=pharmacy_id)
    pharmacy.availability.remove(availability)
    await session.commit()