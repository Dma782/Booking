from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, JSON
from app.database import Base


class Hotel(Base):
    __tablename__ = "hotels"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    location: Mapped[str]
    services: Mapped[list[str]] = mapped_column(JSON)

    rooms: Mapped[list["Room"]] = relationship(back_populates="hotel")


class Room(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))

    name: Mapped[str]
    price: Mapped[int]
    quantity: Mapped[int]
    capacity: Mapped[int] = mapped_column(default=1)
    services: Mapped[list[str]] = mapped_column(JSON, default=list)

    hotel: Mapped["Hotel"] = relationship(back_populates="rooms")
