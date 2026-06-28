from pydantic import BaseModel, EmailStr, Field

class UserAuthSchema(BaseModel):
    email: EmailStr
    password: str = Field(max_length= 30, min_length=6, description="Пароль не менее 6 символов")

class TokenResponseSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class UserResponseSchema(BaseModel):
    id: int
    email: EmailStr
    is_active: bool

    class Config:
        from_attributes = True 