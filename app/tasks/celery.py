from celery import Celery

from app.config import settings

celery_app = Celery(
    "booking_com",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["app.tasks.booking_tasks"],
)
