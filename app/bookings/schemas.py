from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class BaseSchema(BaseModel):
    date_from: datetime
    date_to: datetime

    @field_validator("date_to")
    @classmethod
    def validate_dates(cls, date_to: datetime, info):
        date_from = info.data.get("date_from")
        if date_from and date_to <= date_from:
            raise ValueError("date_to must be later than date_from")
        return date_to


class BookingCreate(BaseSchema):
    room_id: int = Field(ge=1)


class BookingResponse(BaseModel):
    id: int
    user_id: int
    room_id: int
    date_from: datetime
    date_to: datetime
    total_price: int
    status: str

    model_config = ConfigDict(from_attributes=True)


class BookingSearchParams(BaseSchema):
    guests: int = Field(default=1, ge=1)
    services: list[str] = Field(default_factory=list)
    location: str | None = None
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=20, ge=1, le=100)


class AvailableRoomResponse(BaseModel):
    id: int
    hotel_id: int
    hotel_name: str
    name: str
    price: int
    quantity: int
    capacity: int
    services: list[str]
    free_count: int
