from dataclasses import dataclass
from fastapi import FastAPI, HTTPException, status
from typing import Optional, Tuple
from src.utils.auth import get_password_hash
from src.dtos.auth import (
    LoginResponseDTO, RegisterUserRequestDTO, RegisterUserResponseDTO,
    UserResponseDTO, UsersResponseDTO, LoginUserRequestDTO, 
    LoginUserResponseDTO
)
from src.repositories.postgres.auth import AuthRepository, init_auth_repository
from datetime import datetime, timedelta
from passlib.context import CryptContext
import httpx


@dataclass
class AuthService:
    auth_repository: AuthRepository
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def get_all_users(self) -> UsersResponseDTO:
        return await self.auth_repository.get_all_users()

    async def register(
        self,
        email: str,
        username: str,
        password: str,
        telegram_id: str
    ) -> int:
        existing_user = await self.auth_repository.get_user_by_email(email=email)
        
        if existing_user:
            raise HTTPException("Пользователь с таким email или именем уже существует!")
        
        user_dto = RegisterUserRequestDTO(
            email=email,
            username=username,
            hashed_password=get_password_hash(password),
            telegram_id=telegram_id,
        )

        user_id = await self.auth_repository.register(user=user_dto)
        return user_id

    async def login(self, email: str, password: str) -> LoginResponseDTO:
        user = await self.auth_repository.get_user_by_email(email)
        if user and self.pwd_context.verify(password, user.hashed_password):
            user_data = {"sub": user.email}  
            access_token, refresh_token = self.auth_repository.create_tokens(user_data)
            return LoginResponseDTO(
                user_id=user.id,
                access_token=access_token,
                refresh_token=refresh_token,
            )
        return None

    async def refresh_access_token(self, refresh_token: str) -> LoginResponseDTO:
        payload = await self.auth_repository.verify_token(refresh_token)

        if not payload:
            return None 
        
        email = payload.get("sub")  
        
        user = await self.auth_repository.get_user_by_email(email)  
        user_data = {"sub": user.email}  

        if user is None:
            return None  

        access_token, refresh_token = self.auth_repository.create_tokens(user_data)

        return LoginResponseDTO(
            user_id=user.id, 
            access_token=access_token,
            refresh_token=refresh_token,
        )

    async def google_login(self, id_token: str) -> Optional[LoginResponseDTO]:
        # Параметры для проверки ID токена через Google
        client_id = "912264674877-01q28en311jfi4lkj7qao5225pobtlaq.apps.googleusercontent.com"

        # Проверяем токен
        async with httpx.AsyncClient() as client:
            response = await client.get(f'https://oauth2.googleapis.com/tokeninfo?id_token={id_token}')
            user_info = response.json()

        if not response.status_code == 200 or 'email' not in user_info:
            raise HTTPException(status_code=400, detail="Некорректный ID токен!")

        email = user_info['email']
        user = await self.auth_repository.get_user_by_email(email)

        if user is None:
            # Если пользователь не зарегистрирован, можно создать его
            user = RegisterUserRequestDTO(
                email=email,
                username=email.split('@')[0],  # Можно использовать часть email как имя пользователя
                hashed_password=self.get_password_hash(""),  # Установить пароль по умолчанию или оставить пустым
                telegram_id="",  # Можно оставить пустым
            )
            await self.auth_repository.register(user=user)

        user_data = {"sub": user.email}
        access_token, refresh_token = self.auth_repository.create_tokens(user_data)

        return LoginResponseDTO(
            user_id=user.id,
            access_token=access_token,
            refresh_token=refresh_token,
        )
    
    async def get_user_by_email(self, email) -> UserResponseDTO:
        user =  await self.auth_repository.get_user_by_email(email=email)
        return UserResponseDTO(
            id=user.id,
            email=user.email,
            username=user.username,
            hashed_password=user.hashed_password,
            telegram_id=user.telegram_id,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

def get_auth_service(auth_repository: AuthRepository = init_auth_repository()) -> AuthService:
    auth_service = AuthService(auth_repository=auth_repository)
    return auth_service
