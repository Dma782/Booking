from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.bookings.schemas import (
    AvailableRoomResponse, 
    BookingCreate,
    BookingResponse,
    BookingSearchParams,
)
from app.bookings.service import BookingService
from app.database import get_db_session
from app.tasks.booking_tasks import send_booking_confirmation
from app.users.auth import get_current_user
from app.users.models import User

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("/rooms", response_model=list[AvailableRoomResponse])
async def search_available_rooms(
    date_from: datetime,
    date_to: datetime,
    guests: int = Query(default=1, ge=1),
    services: list[str] = Query(default_factory=list),
    location: str | None = None,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    session: AsyncSession = Depends(get_db_session),
):
    params = BookingSearchParams(
        date_from=date_from.replace(tzinfo=None),
        date_to=date_to.replace(tzinfo=None),
        guests=guests,
        services=services,
        location=location,
        page=page,
        limit=limit,
    )
    return await BookingService.search_available_rooms(session=session, params=params)


@router.post("", response_model=BookingResponse, status_code=201)
async def create_booking(
    data: BookingCreate,
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    booking = await BookingService.create_booking(
        session=session,
        user=current_user,
        data=data,
    )
    try:
        send_booking_confirmation.delay(current_user.email)
    except Exception:
        pass
    return booking


@router.get("/me", response_model=list[BookingResponse])
async def get_my_bookings(
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    return await BookingService.get_my_bookings(session=session, user=current_user)


@router.patch("/{booking_id}/cancel", response_model=BookingResponse)
async def cancel_booking(
    booking_id: int,
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    return await BookingService.cancel_booking(
        session=session,
        user=current_user,
        booking_id=booking_id,
    )
