from datetime import datetime
from src.dtos.base import BaseResponseDTO, BaseRequestDTO
from pydantic import EmailStr


class UserRequestDTO(BaseRequestDTO):
    id: int


class LoginUserRequestDTO(BaseRequestDTO):
    email: EmailStr
    password: str


class LoginUserResponseDTO(BaseResponseDTO):
    user_id: int
    access_token: str
    refresh_token: str


class RegisterUserRequestDTO(BaseRequestDTO):
    username: str
    email: EmailStr
    hashed_password: str
    telegram_id: str


class RegisterUserResponseDTO(BaseResponseDTO):
    user_id: int


class UserResponseDTO(BaseResponseDTO):
    id: int
    username: str
    email: EmailStr
    hashed_password: str
    telegram_id: str
    created_at: datetime
    updated_at: datetime


class UsersResponseDTO(BaseResponseDTO):
    items: list[UserResponseDTO]

    
class LoginResponseDTO(BaseResponseDTO):
    user_id: int
    access_token: str
    refresh_token: str
