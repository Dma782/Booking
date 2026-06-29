from math import ceil

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.bookings.dao import ACTIVE_STATUS, BookingDAO
from app.bookings.models import Booking
from app.bookings.schemas import (
    AvailableRoomResponse,
    BookingCreate,
    BookingSearchParams,
)
from app.users.models import User


class BookingService:
    @classmethod
    async def create_booking(
        cls,
        session: AsyncSession,
        user: User,
        data: BookingCreate,
    ) -> Booking:
        try:
            room = await BookingDAO.get_room_for_update(session, data.room_id)
            if not room:
                raise HTTPException(status_code=404, detail="Room not found")

            booked_count = await BookingDAO.count_booked_rooms(
                session=session,
                room_id=data.room_id,
                date_from=data.date_from,
                date_to=data.date_to,
            )
            if booked_count >= room.quantity:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="This room is already booked for selected time",
                )

            hours = ceil((data.date_to - data.date_from).total_seconds() / 3600)
            booking = Booking(
                user_id=user.id,
                room_id=data.room_id,
                date_from=data.date_from,
                date_to=data.date_to,
                total_price=max(1, hours) * room.price,
                status=ACTIVE_STATUS,
            )
            session.add(booking)
            await session.flush()
            await session.commit()

            return booking
        except Exception:
            await session.rollback()
            raise

    @classmethod
    async def get_my_bookings(cls, session: AsyncSession, user: User) -> list[Booking]:
        return await BookingDAO.get_user_bookings(session=session, user_id=user.id)

    @classmethod
    async def cancel_booking(
        cls,
        session: AsyncSession,
        user: User,
        booking_id: int,
    ) -> Booking:
        try:
            booking = await BookingDAO.get_user_booking_for_update(
                session=session,
                booking_id=booking_id,
                user_id=user.id,
            )
            if not booking:
                raise HTTPException(status_code=404, detail="Booking not found")
            if booking.status != ACTIVE_STATUS:
                raise HTTPException(status_code=400, detail="Booking is not active")

            booking.status = "cancelled"
            await session.flush()
            await session.commit()

            return booking
        except Exception:
            await session.rollback()
            raise

    @classmethod
    async def search_available_rooms(
        cls,
        session: AsyncSession,
        params: BookingSearchParams,
    ) -> list[AvailableRoomResponse]:
        rows = await BookingDAO.find_available_rooms(
            session=session,
            date_from=params.date_from,
            date_to=params.date_to,
            guests=params.guests,
            location=params.location,
            page=params.page,
            limit=params.limit,
        )

        required_services = set(params.services)
        rooms = []
        for room, hotel, free_count in rows:
            room_services = set(room.services or [])
            hotel_services = set(hotel.services or [])
            if required_services and not required_services.issubset(
                room_services | hotel_services
            ):
                continue

            rooms.append(
                AvailableRoomResponse(
                    id=room.id,
                    hotel_id=hotel.id,
                    hotel_name=hotel.name,
                    name=room.name,
                    price=room.price,
                    quantity=room.quantity,
                    capacity=room.capacity,
                    services=sorted(room_services | hotel_services),
                    free_count=free_count,
                )
            )

        return rooms
