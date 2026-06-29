# Booking backend

FastAPI backend for hotel and room bookings.

## Local start without Docker

1. Create PostgreSQL database `booking_com`.
2. Copy `.env.example` to `.env` and set database credentials.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Apply migrations:

```bash
alembic upgrade head
```

5. Add demo data:

```bash
python scripts/seed.py
```

6. Run API:

```bash
uvicorn app.main:app --reload
```

7. Optional background worker:

```bash
celery -A app.tasks.celery.celery_app worker --loglevel=info
```

Redis is needed only for Celery tasks. API booking creation still works if Redis is not running.

## Useful endpoints

- `GET /health`
- `POST /auth/register`
- `POST /auth/login`
- `POST /auth/refresh`
- `GET /auth/me`
- `GET /hotels`
- `POST /hotels`
- `GET /hotels/rooms`
- `POST /hotels/rooms`
- `GET /bookings/rooms`
- `POST /bookings`
- `GET /bookings/me`
- `PATCH /bookings/{booking_id}/cancel`
