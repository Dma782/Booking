from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db_session
from app.hotels.dao import HotelDAO, RoomDAO
from app.hotels.schemas import SHotelResponse, SRoomResponse
from typing import List

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("/get_hotels", response_model=List[SHotelResponse])
async def get_all_hotels(session: AsyncSession = Depends(get_db_session)):
    hotels = await HotelDAO.get_all(async_session=session)
    return hotels


@router.get("/get_rooms", response_model=List[SRoomResponse])
async def get_all_rooms(session: AsyncSession = Depends(get_db_session)):
    hotels = await RoomDAO.get_all(async_session=session)
    return hotels
