from datetime import datetime
from typing import List
from pydantic import BaseModel, EmailStr


class SRegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    telegram_id: str

class SRegisterResponse(BaseModel):
    user_id: int

class SUserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    telegram_id: str
    created_at: datetime
    updated_at: datetime

class User(BaseModel):
    user_id: int
    message: str

class SUsersResponse(BaseModel):
    items: List[SUserResponse]

class SLoginResponse(BaseModel):
    user_id: int
    access_token: str
    refresh_token: str
    type: str

class SLoginRequest(BaseModel):
    email: EmailStr
    password: str

class SOauthLoginRequest(BaseModel):
    id_token: str

class SRefreshTokenRequest(BaseModel):
    refresh_token: str