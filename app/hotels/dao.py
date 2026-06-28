from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.hotels.models import Hotel, Room


class BaseDAO:
    model = None

    @classmethod
    async def get_all(cls, session: AsyncSession) -> list:
        query = select(cls.model)
        result = await session.execute(query)
        return result.scalars().all()


class HotelDAO(BaseDAO):
    model = Hotel


class RoomDAO(BaseDAO):
    model = Room
