import asyncio
import sys
from pathlib import Path

from sqlalchemy import select

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.database import async_session_maker
from app.hotels.models import Hotel, Room


async def seed() -> None:
    async with async_session_maker() as session:
        result = await session.execute(select(Hotel).limit(1))
        if result.scalar_one_or_none():
            print("Seed data already exists")
            return

        hotel = Hotel(
            name="Local Business Center",
            location="Kyiv",
            services=["wifi", "parking", "coffee"],
        )
        session.add(hotel)
        await session.flush()

        session.add_all(
            [
                Room(
                    hotel_id=hotel.id,
                    name="Meeting Room A",
                    price=300,
                    quantity=1,
                    capacity=5,
                    services=["projector", "whiteboard"],
                ),
                Room(
                    hotel_id=hotel.id,
                    name="Conference Hall",
                    price=900,
                    quantity=2,
                    capacity=20,
                    services=["projector", "sound", "stage"],
                ),
            ]
        )
        await session.commit()
        print("Seed data created")


if __name__ == "__main__":
    asyncio.run(seed())
