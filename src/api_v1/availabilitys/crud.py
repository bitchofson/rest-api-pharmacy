import uuid

from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.availability import AvailabilityORM
from core.models.pharmacy import PharmacyORM
from core.models.drug import DrugORM

from ..availability_pharmacys_schemes import AvailabilityCreateSchema, AvailabilityUpdateSchema, AvailabilityUpdatePartialSchema

async def get_availabilitys(session: AsyncSession) -> list[AvailabilityORM]:
    stmt = (
        select(AvailabilityORM)
            .options(
                selectinload(AvailabilityORM.drug)
                .options(
                    selectinload(DrugORM.release_form),
                    selectinload(DrugORM.manufacturer)
                ),
                selectinload(AvailabilityORM.pharmacy)
                )
            )

    result: Result = await session.execute(stmt)
    result_orm = result.scalars().all()
    return list(result_orm)

async def get_availability(
        session: AsyncSession,
        availability_id: uuid.UUID
) -> AvailabilityORM | None:
    stmt = (
        select(AvailabilityORM)
            .options(
                selectinload(AvailabilityORM.drug)
                    .options(
                        selectinload(DrugORM.release_form),
                        selectinload(DrugORM.manufacturer)
                    ),
                selectinload(AvailabilityORM.pharmacy)
            ).where(AvailabilityORM.id == availability_id)
    )

    result: Result = await session.execute(stmt)
    result_orm = result.scalar_one_or_none()
    return result_orm

async def create_availability(
        session: AsyncSession,
        availability_in: AvailabilityCreateSchema
) -> AvailabilityORM:
    availability = AvailabilityORM(**availability_in.model_dump())
    session.add(availability)
    await session.commit()
    return availability

async def update_availability(
        session: AsyncSession,
        availability: AvailabilityORM,
        availability_update: AvailabilityUpdateSchema | AvailabilityUpdatePartialSchema,
        partial: bool = False
) -> AvailabilityORM:
    for name, value in availability_update.model_dump(exclude_unset=partial).items():
        setattr(availability, name, value)
    await session.commit()
    return availability

async def delete_availability(
        session: AsyncSession,
        availability: AvailabilityORM
) -> None:
    await session.delete(availability)
    await session.commit();

async def add_pharmacy_in_available(
        availability_id: uuid.UUID,
        session: AsyncSession,
        pharmacy: PharmacyORM,
):
    availability = await get_availability(session, availability_id)
    availability.pharmacy.append(pharmacy)
    await session.commit()
    return availability

async def delete_pharmacy_from_available(
        availability_id: uuid.UUID,
        session: AsyncSession,
        pharmacy: PharmacyORM,
):
    availability = await get_availability(session, availability_id)
    availability.pharmacy.remove(pharmacy)
    await session.commit()