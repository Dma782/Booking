from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserAuthSchema(BaseModel):
    email: EmailStr
    password: str = Field(max_length= 30, min_length=6, description="Пароль не менее 6 символов")

    model_config = ConfigDict(from_attributes=True)

class TokenResponseSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

    model_config = ConfigDict(from_attributes=True)

class UserResponseSchema(BaseModel):
    id: int
    email: EmailStr
    is_active: bool

    model_config = ConfigDict(from_attributes=True)