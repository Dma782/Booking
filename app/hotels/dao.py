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

    @classmethod
    async def add(
        cls,
        session: AsyncSession,
        name: str,
        location: str,
        services: list[str],
    ) -> Hotel:
        hotel = Hotel(name=name, location=location, services=services)
        session.add(hotel)
        await session.commit()
        await session.refresh(hotel)
        return hotel


class RoomDAO(BaseDAO):
    model = Room

    @classmethod
    async def add(
        cls,
        session: AsyncSession,
        hotel_id: int,
        name: str,
        price: int,
        quantity: int,
        capacity: int,
        services: list[str],
    ) -> Room:
        room = Room(
            hotel_id=hotel_id,
            name=name,
            price=price,
            quantity=quantity,
            capacity=capacity,
            services=services,
        )
        session.add(room)
        await session.commit()
        await session.refresh(room)
        return room
