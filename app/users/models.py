from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, JSON
from app.database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)

    refresh_tokens: Mapped[list["Refresh_token"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )


class Refresh_token(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    expire: Mapped[datetime]
    jti: Mapped[str] = mapped_column(unique=True, index=True)

    user: Mapped["User"] = relationship(back_populates="refresh_tokens")
