from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserSignup(BaseModel):
    full_name: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=50)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    role: str
    is_active: bool

    subscription: Optional[str] = None
    api_key: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)