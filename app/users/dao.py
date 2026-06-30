from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, select
from datetime import datetime
from app.users.models import User, Refresh_token


class UsersDAO:
    @classmethod
    async def add_user(
        cls, session: AsyncSession, email: str, hashed_password: str
    ) -> User:
        new_user = User(email=email, hashed_password=hashed_password)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user

    @classmethod
    async def find_by_email(cls, session: AsyncSession, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()


class Refresh_token_DAO:
    @classmethod
    async def add_token(
        cls,
        session: AsyncSession,
        user_id: int,
        jti: str,
        expire: datetime,
        commit: bool = True,
    ):
        new_token = Refresh_token(user_id=user_id, jti=jti, expire=expire)
        session.add(new_token)
        if commit:
            await session.commit()
        return new_token

    @classmethod
    async def find_by_jti(cls, session: AsyncSession, jti: str) -> Refresh_token | None:
        stmt = select(Refresh_token).where(Refresh_token.jti == jti)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @classmethod
    async def find_by_jti_for_update(
        cls, session: AsyncSession, jti: str
    ) -> Refresh_token | None:
        stmt = select(Refresh_token).where(Refresh_token.jti == jti).with_for_update()
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @classmethod
    async def delete_token_by_jti(cls, session: AsyncSession, jti: str):
        stmt = delete(Refresh_token).where(Refresh_token.jti == jti)
        await session.execute(stmt)
        await session.commit()
