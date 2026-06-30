from app.tasks.celery import celery_app
from app.tasks.email_services import send_booking_email

@celery_app.task
def send_booking_confirmation(email: str):
    send_booking_email(email)