from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
from jose import JWTError, jwt
from src.dtos.auth import UserResponseDTO
from src.core.config import settings
from fastapi import status, HTTPException, Request, Response, Depends


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        return payload  # Если все хорошо, возвращаем полезную нагрузку
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

async def get_refresh_token(request: Request):
    token = request.cookies.get("refresh_token")
    print(token)
    if not token:
        print("Error 1")
        raise HTTPException(status_code=401)
    return token

async def get_current_user(token: str = Depends(get_refresh_token)) -> UserResponseDTO:
    from src.services.postgres.auth import get_auth_service
    service = get_auth_service()

    try:
        payload = jwt.decode(
            token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm]
        )
    except JWTError:
        raise HTTPException(status_code=401)
    
    expire: str = payload.get("exp")
    
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise HTTPException(status_code=401)
    email: str = payload.get("sub")
    
    if not email:
        raise HTTPException(status_code=401)
    user = await service.get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=401)
    
    return UserResponseDTO(
        id=user.id,
        email=user.email,
        username=user.username,
        hashed_password=user.hashed_password,
        telegram_id=user.telegram_id,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )