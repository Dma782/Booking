from app.tasks.celery import celery_app


@celery_app.task(name="send_booking_confirmation")
def send_booking_confirmation(booking_id: int) -> dict:
    # Here you can generate a PDF ticket, send email and update bonuses.
    return {"booking_id": booking_id, "status": "processed"}
