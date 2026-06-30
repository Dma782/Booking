from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.bookings.models import Booking
from app.hotels.models import Hotel, Room

ACTIVE_STATUS = "confirmed"


class BookingDAO:
    # занимает и лочит комнату что бы нельзя было заказать одновременно одну и ту же комнату
    @classmethod
    async def get_room_for_update(        #
        cls, session: AsyncSession, room_id: int
    ) -> Room | None:
        query = select(Room).where(Room.id == room_id).with_for_update()
        result = await session.execute(query)
        return result.scalar_one_or_none()

    #Сколько номеров уже занято в данном временном диапазоне
    @classmethod
    async def count_booked_rooms(
        cls,
        session: AsyncSession,
        room_id: int,
        date_from: datetime,
        date_to: datetime,
    ) -> int:
        query = select(func.count(Booking.id)).where(
            Booking.room_id == room_id,
            Booking.status == ACTIVE_STATUS,
            Booking.date_from < date_to,
            Booking.date_to > date_from,
        )
        result = await session.execute(query)
        return result.scalar_one()

    #Возвращает все брони пользователя
    @classmethod
    async def get_user_bookings(
        cls, session: AsyncSession, user_id: int
    ) -> list[Booking]:
        query = (
            select(Booking)
            .where(Booking.user_id == user_id)
            .order_by(Booking.date_from.desc())
        )
        result = await session.execute(query)
        return list(result.scalars().all())

    #лочит booking пользователя
    @classmethod
    async def get_user_booking_for_update(
        cls,
        session: AsyncSession,
        booking_id: int,
        user_id: int,
    ) -> Booking | None:
        query = (
            select(Booking)
            .where(Booking.id == booking_id, Booking.user_id == user_id)
            .with_for_update()
        )
        result = await session.execute(query)
        return result.scalar_one_or_none()

    # исчет свободные комнаты тяжелым скьюл запросом с подзапросом
    @classmethod
    async def find_available_rooms(
        cls,
        session: AsyncSession,
        date_from: datetime,
        date_to: datetime,
        guests: int,
        location: str | None,
        page: int,
        limit: int,
    ) -> list[tuple[Room, Hotel, int]]:
        booked = (
            select(Booking.room_id, func.count(Booking.id).label("booked_count"))
            .where(
                Booking.status == ACTIVE_STATUS,
                Booking.date_from < date_to,
                Booking.date_to > date_from,
            )
            .group_by(Booking.room_id)
            .subquery()
        )

        free_count = Room.quantity - func.coalesce(booked.c.booked_count, 0)
        query = (
            select(Room, Hotel, free_count.label("free_count"))
            .join(Hotel, Hotel.id == Room.hotel_id)
            .outerjoin(booked, booked.c.room_id == Room.id)
            .where(Room.capacity >= guests, free_count > 0)
            .order_by(Room.price, Room.id)
            .offset((page - 1) * limit)
            .limit(limit)
        )

        if location:
            query = query.where(Hotel.location.ilike(f"%{location}%"))

        result = await session.execute(query)
        return list(result.all())
