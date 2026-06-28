from fastapi import FastAPI
from app.hotels.router import router as hotel_router
from app.users.router import router as auth_router

app = FastAPI()
app.include_router(hotel_router)
app.include_router(auth_router)
