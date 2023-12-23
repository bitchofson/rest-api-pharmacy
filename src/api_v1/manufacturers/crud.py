import uuid

from sqlalchemy import select, or_
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.manufacturer import ManufacturerORM

from .schemas import ManufacturerCreateSchema, ManufacturerUpdateSchema, ManufacturerUpdatePartialSchema


async def get_manufacturers(session: AsyncSession, filter: str) -> [ManufacturerORM]:
    stmt = select(ManufacturerORM).order_by(ManufacturerORM.id)
    if filter is not None and filter != 'null':
            criteria = dict(x.split("*") for x in filter.split('-'))
            criteria_list = []

            for attr, value in criteria.items():
                _attr = getattr(ManufacturerORM, attr)
                search = '%{}%'.format(value)
                criteria_list.append(_attr.like(search))
                
            stmt = stmt.filter(or_(*criteria_list))
    
    result: Result = await session.execute(stmt)
    manufacturers = result.scalars().all()
    return list(manufacturers)

async def get_manufacturer(
        session: AsyncSession,
        manufacturer_id: uuid.UUID) -> ManufacturerORM | None:
    return await session.get(ManufacturerORM, manufacturer_id)

async def create_manufacturer(
        session: AsyncSession,
        manufacturer_in: ManufacturerCreateSchema
) -> ManufacturerORM:
    manufacturer = ManufacturerORM(**manufacturer_in.model_dump())
    session.add(manufacturer)
    await session.commit()
    #await session.refresh(release_form)
    return manufacturer

async def update_manufacturer(
        session: AsyncSession,
        manufacturer: ManufacturerORM,
        manufacturer_update: ManufacturerUpdateSchema | ManufacturerUpdatePartialSchema,
        partial: bool = False
) -> ManufacturerORM:
    for name, value in manufacturer_update.model_dump(exclude_unset=partial).items():
        setattr(manufacturer, name, value)
    await session.commit()
    return manufacturer


async def delete_manufacturer(
        session: AsyncSession,
        manufacturer: ManufacturerORM
) -> None:
    await session.delete(manufacturer)
    await session.commit()