from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import CheckConstraint, ForeignKey, Index
from app.database import Base


class Booking(Base):
    __tablename__ = "bookings"
    __table_args__ = (
        CheckConstraint("date_to > date_from", name="check_booking_dates"),
        Index("ix_bookings_room_dates", "room_id", "date_from", "date_to"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    date_from: Mapped[datetime]
    date_to: Mapped[datetime]
    total_price: Mapped[int]
    status: Mapped[str] = mapped_column(default="confirmed")
