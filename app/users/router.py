from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
from jose import jwt, JWTError, ExpiredSignatureError
from fastapi.security import OAuth2PasswordRequestForm

from app.database import get_db_session
from app.config import settings


from app.users.schemas import UserAuthSchema, TokenResponseSchema, UserResponseSchema, RefreshTokenRequestSchema
from app.users.dao import UsersDAO, Refresh_token_DAO
from app.users.models import User


from app.users.auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
    get_current_user,
    utc_now_naive,
)

router = APIRouter(prefix="/auth", tags=["Аутентификация"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserAuthSchema, session: AsyncSession = Depends(get_db_session)
):
    existing_user = await UsersDAO.find_by_email(session, user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exist")
    hashed_pwd = get_password_hash(user_data.password)
    await UsersDAO.add_user(session, email=user_data.email, hashed_password=hashed_pwd)

    return {"message": "Succesfull register"}


@router.post("/login", response_model=TokenResponseSchema)
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_db_session),
):
    user = await UsersDAO.find_by_email(session, form_data.username) # в форм_дате в юзернейм мы вводим емейл
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Неверная почта или пароль")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Пользователь деактивирован")

    access_token = create_access_token(user.id)
    refresh_token, refresh_jti = create_refresh_token(user.id)

    expire_time = utc_now_naive() + timedelta(days=30)

    await Refresh_token_DAO.add_token(
        session, user_id=user.id, jti=refresh_jti, expire=expire_time
    )

    return {"access_token": access_token, "refresh_token": refresh_token}


@router.post("/refresh", response_model=TokenResponseSchema)
async def refresh_tokens(
    request_refresh_token: RefreshTokenRequestSchema,
    session: AsyncSession = Depends(get_db_session),
):
    try:
        refresh_token = jwt.decode(
            request_refresh_token.refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        jti: str = refresh_token.get("jti")
        token_type: str = refresh_token.get("type")
        user_id: str = refresh_token.get("sub")

        if token_type != "refresh" or not jti or not user_id:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh токен истек")
    except JWTError:
        raise HTTPException(status_code=401, detail="Refresh token expired")

    try:
        db_token = await Refresh_token_DAO.find_by_jti_for_update(session, jti)
        if not db_token:
            raise HTTPException(
                status_code=401, detail="Токен не найден или уже был использован"
            )
        if db_token.expire < utc_now_naive():
            await session.delete(db_token)
            await session.commit()
            raise HTTPException(status_code=401, detail="Refresh токен истек")

        await session.delete(db_token)

        new_access = create_access_token(int(user_id))
        new_refresh, new_refresh_jti = create_refresh_token(int(user_id))

        expire_time = utc_now_naive() + timedelta(days=30)
        await Refresh_token_DAO.add_token(
            session,
            user_id=int(user_id),
            jti=new_refresh_jti,
            expire=expire_time,
            commit=False,
        )
        await session.commit()
    except Exception:
        await session.rollback()
        raise

    return {"access_token": new_access, "refresh_token": new_refresh}


@router.post("/logout")
async def logout_user(
    refresh_token: str = Body(embed=True),
    session: AsyncSession = Depends(get_db_session),
):
    try:
        refresh_token = jwt.decode(
            refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        jti: str = refresh_token.get("jti")
        if jti:
            await Refresh_token_DAO.delete_token_by_jti(session, jti)
    except JWTError:
        pass

    return {"message": "Вы успешно вышли из системы"}


@router.get("/me", response_model=UserResponseSchema)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user
