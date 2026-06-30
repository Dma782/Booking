from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db_session
from app.hotels.dao import HotelDAO, RoomDAO
from app.hotels.schemas import SHotelCreate, SHotelResponse, SRoomCreate, SRoomResponse
from typing import List

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.post("", response_model=SHotelResponse, status_code=status.HTTP_201_CREATED)
async def create_hotel(
    hotel_data: SHotelCreate,
    session: AsyncSession = Depends(get_db_session),
):
    return await HotelDAO.add(
        session=session,
        name=hotel_data.name,
        location=hotel_data.location,
        services=list(hotel_data.services),
    )


@router.post(
    "/rooms", response_model=SRoomResponse, status_code=status.HTTP_201_CREATED
)
async def create_room(
    room_data: SRoomCreate,
    session: AsyncSession = Depends(get_db_session),
):
    return await RoomDAO.add(
        session=session,
        hotel_id=room_data.hotel_id,
        name=room_data.name,
        price=room_data.price,
        quantity=room_data.quantity,
        capacity=room_data.capacity,
        services=room_data.services,
    )

@router.get("", response_model=List[SHotelResponse])
async def list_hotels(session: AsyncSession = Depends(get_db_session)):
    return await HotelDAO.get_all(session=session)


@router.get("/rooms", response_model=List[SRoomResponse])
async def list_rooms(session: AsyncSession = Depends(get_db_session)):
    return await RoomDAO.get_all(session=session)
