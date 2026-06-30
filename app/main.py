from fastapi import FastAPI
from app.hotels.router import router as hotel_router
from app.users.router import router as auth_router
from app.bookings.router import router as booking_router

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(hotel_router) 
app.include_router(auth_router)
app.include_router(booking_router)


@app.get("/health", tags=["Сервис"])
async def health_check():
    return {"status": "ok"}