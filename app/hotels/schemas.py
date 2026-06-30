from pydantic import BaseModel, ConfigDict, Field


class SHotel(BaseModel):
    name: str = Field(min_length=3, max_length=50, description="Name of the hotel")
    location: str
    services: list[str] = Field(default_factory=list)
    model_config = ConfigDict(from_attributes=True)


class SHotelCreate(SHotel):
    pass


class SHotelResponse(SHotelCreate):
    id: int


class SRoom(BaseModel):
    hotel_id: int = Field(ge=1)
    name: str
    price: int = Field(ge=1)
    quantity: int = Field(ge=1)
    capacity: int = Field(default=1, ge=1)
    services: list[str] = Field(default_factory=list)
    model_config = ConfigDict(from_attributes=True)


class SRoomCreate(SRoom):
    pass


class SRoomResponse(SRoomCreate):
    id: int
