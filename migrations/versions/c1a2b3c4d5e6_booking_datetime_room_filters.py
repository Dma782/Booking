"""booking datetime and room filters

Revision ID: c1a2b3c4d5e6
Revises: b93990348848
Create Date: 2026-06-29 00:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "c1a2b3c4d5e6"
down_revision: Union[str, Sequence[str], None] = "b93990348848"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "rooms",
        sa.Column("capacity", sa.Integer(), nullable=False, server_default="1"),
    )
    op.add_column(
        "rooms",
        sa.Column(
            "services",
            sa.JSON(),
            nullable=False,
            server_default=sa.text("'[]'::json"),
        ),
    )
    op.alter_column(
        "bookings",
        "date_from",
        existing_type=sa.Date(),
        type_=sa.DateTime(),
        existing_nullable=False,
        postgresql_using="date_from::timestamp",
    )
    op.alter_column(
        "bookings",
        "date_to",
        existing_type=sa.Date(),
        type_=sa.DateTime(),
        existing_nullable=False,
        postgresql_using="date_to::timestamp",
    )
    op.create_check_constraint(
        "check_booking_dates",
        "bookings",
        "date_to > date_from",
    )
    op.create_index(
        "ix_bookings_room_dates",
        "bookings",
        ["room_id", "date_from", "date_to"],
    )


def downgrade() -> None:
    op.drop_index("ix_bookings_room_dates", table_name="bookings")
    op.drop_constraint("check_booking_dates", "bookings", type_="check")
    op.alter_column(
        "bookings",
        "date_to",
        existing_type=sa.DateTime(),
        type_=sa.Date(),
        existing_nullable=False,
        postgresql_using="date_to::date",
    )
    op.alter_column(
        "bookings",
        "date_from",
        existing_type=sa.DateTime(),
        type_=sa.Date(),
        existing_nullable=False,
        postgresql_using="date_from::date",
    )
    op.drop_column("rooms", "services")
    op.drop_column("rooms", "capacity")
