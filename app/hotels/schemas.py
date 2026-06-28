from pydantic import BaseModel, ConfigDict, Field


class SHotel(BaseModel):
    name: str = Field(min_length=3, max_length=50, description="Name of the hotel")
    location: str
    services: list[str] | dict
    model_config = ConfigDict(from_attributes=True)


class SHotelCreate(SHotel):
    pass


class SHotelResponse(SHotelCreate):
    id: int


class SRoom(BaseModel):
    hotel_id: int
    name: str
    price: int
    quantity: int
    model_config = ConfigDict(from_attributes=True)


class SRoomCreate(SRoom):
    pass


class SRoomResponse(SRoomCreate):
    id: int
