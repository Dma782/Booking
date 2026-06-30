import resend
from app.config import settings

resend.api_key = settings.RESEND_API_KEY


def send_booking_email(to_email: str):
    params = {
        "from": "onboarding@resend.dev",
        "to": [to_email],
        "subject": "Booking confirmed",
        "html": "<p>Your booking is confirmed!</p>",
    }

    email = resend.Emails.send(params)
    return email