1. Create PostgreSQL database `database`.
2. Copy `.env.example` to `.env` and set database credentials.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Apply migrations:

```bash
alembic upgrade head
```

5. Run API:

```bash
uvicorn app.main:app --reload
```

6. Run Celery:
```bash

```


## endpoints

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
