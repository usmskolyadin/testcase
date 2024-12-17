from dataclasses import dataclass
from datetime import datetime, timedelta
from http.client import HTTPException
from typing import Dict, Iterable, Optional, Tuple

from src.models.auth import User
from sqlalchemy import Executable, select, func, delete

from src.dtos.auth import (
    UserRequestDTO,
    UsersResponseDTO,
    RegisterUserRequestDTO,
    RegisterUserResponseDTO,
    UserResponseDTO,
)
from src.models.auth import User
from src.repositories.postgres.base import SQLAlchemyRepository
from jose import JWTError, jwt
from src.core.config import settings


@dataclass
class AuthRepository(SQLAlchemyRepository):
    async def get_user(self, request: UserRequestDTO) -> UserResponseDTO | None:
        model: User | None = await self.get(User, request.id)
        return UserResponseDTO(
            id=model.id,
            title=model.title,
            picture_url=model.picture_url,
            description=model.description,
            views=0,
            likes=0,
            type=model.type,
            created_at=model.created_at,
            updated_at=model.updated_at
        ) if model else None
    
    async def get_all_users(self) -> UsersResponseDTO:
        query: Executable = select(User)
        models: Iterable[User] = await self.scalars(query)
        return UsersResponseDTO(items=[UserResponseDTO.from_orm(model) for model in models])

    async def register(self, user: RegisterUserRequestDTO) -> RegisterUserResponseDTO:
        model = User(
            username=user.username,
            email=user.email,
            hashed_password=user.hashed_password,
            telegram_id=user.telegram_id
        )
        await self.add(model)
        return RegisterUserResponseDTO(user_id=model.id)

    async def get_user_by_id(self, user_id: str) -> Optional[UserResponseDTO]:
        user = await self.scalars(select(User).where(User.id == user_id)).first()
        if user:
            return UserResponseDTO.from_orm(user)
        return None

    async def get_user_by_email(self, email: str) -> Optional[UserResponseDTO]:
        user_result = await self.scalars(select(User).where((User.email == email)))
        user = user_result.first()
        if user:
            return UserResponseDTO.from_orm(user)
        return None

    def create_tokens(self, data: Dict[str, str]) -> Tuple[str, str]:
        if not isinstance(data, dict):
            raise ValueError("data must be a dictionary")

        access_token = self.create_access_token(data)
        refresh_token = self.create_refresh_token(data)
        return access_token, refresh_token

    def create_access_token(self, data: Dict[str, str], expires_delta: timedelta = None) -> str:
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.jwt_access_token_expire_minutes)
        to_encode = {'exp': expire, **data}
        return jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

    def create_refresh_token(self, data: Dict[str, str], expires_delta: timedelta = None) -> str:
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.jwt_refresh_token_expire_minutes)
        to_encode = {'exp': expire, **data}
        return jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


    def decode_token(self, token: str) -> Dict[str, str]:
        return jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])

    async def refresh_tokens(self, refresh_token: str) -> Optional[Tuple[str, str]]:
        try:
            payload = self.decode_token(refresh_token)
            # Здесь можно добавить логику для проверки, существует ли пользователь
            token_data = {"sub": payload.get("sub")}
            # Создаем новую пару токенов
            new_access_token, new_refresh_token = self.create_tokens(token_data)
            return new_access_token, new_refresh_token
        except jwt.ExpiredSignatureError:
            return None  # Рефреш токен истек
        except Exception as e:
            return None  # Ошибка декодирования

    async def verify_token(self, token: str):
        try:
            # Декодируем токен
            payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
            return payload  # Если все хорошо, возвращаем полезную нагрузку

        except Exception as e:
            return print(e)

def init_auth_repository() -> AuthRepository:
    return AuthRepository()
