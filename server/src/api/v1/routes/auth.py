from datetime import timedelta
from fastapi import UploadFile, File, APIRouter, Depends, status, HTTPException, Response
from src.services.postgres.auth import get_auth_service
from src.api.v1.schemas.auth import (
        SLoginRequest, SLoginResponse, SRefreshTokenRequest, SRegisterRequest, SRegisterResponse, SUserResponse, SUsersResponse
    )


router = APIRouter(prefix="/auth", tags=["Authentication & OAuth"]) 


@router.get(
    path="/users",
    summary="List of users",
    response_model=SUsersResponse,
    status_code=status.HTTP_200_OK,
    # responses={status.HTTP_200_OK: {"models": SUsersResponse}},
)
async def get_all_users() -> SUsersResponse:
    service = get_auth_service()
    users = await service.get_all_users()
    items = list(map(
        lambda user: SUserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            telegram_id=user.telegram_id,
            created_at=user.created_at,
            updated_at=user.updated_at,
        ),
        users.items
    ))

    return SUsersResponse(items=items)

@router.post(
    path="/register",
    summary="Register through email and password",
    response_model=SRegisterResponse,
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_200_OK: {"model": SRegisterResponse}},
)
async def register_user(
    data: SRegisterRequest,
) -> SRegisterResponse:
    
    service = get_auth_service()

    user = await service.register(
        username=data.username,
        email=data.email,
        password=data.password,
        telegram_id=data.telegram_id,
    )
    return SRegisterResponse(user_id=user.user_id)

@router.post(
    path="/login",
    summary="Auth with jwt through email and password",
    response_model=SLoginResponse,
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_200_OK: {"model": SLoginResponse}},
)
async def login_user(
    data: SLoginRequest,
    response: Response
) -> SLoginResponse:
    service = get_auth_service()
    tokens = await service.login(
        email=data.email,
        password=data.password,
    )
    if tokens is None:
        raise HTTPException(status_code=401, detail="Invalid credentials!")
    
    response.set_cookie(key="refresh_token", 
                        value=tokens.refresh_token, 
                        httponly=True, 
                        max_age=timedelta(days=30).total_seconds()
                        )
    return SLoginResponse(
        user_id=tokens.user_id,
        access_token=tokens.access_token,
        refresh_token=tokens.refresh_token,
        type="Baerer"
    )

@router.post(
    path="/refresh-token",
    summary="Refresh access and refresh tokens",
    response_model=SLoginResponse,
    status_code=status.HTTP_200_OK,
)
async def refresh_token(
    token: SRefreshTokenRequest,
    response: Response
) -> SLoginResponse:
    
    service = get_auth_service()

    tokens = await service.refresh_access_token(
        refresh_token=token.refresh_token,
    )
    
    if tokens is None:
        raise HTTPException(status_code=401, detail="Invalid refresh token!")
    
    response.set_cookie(key="refresh_token", 
                        value=tokens.refresh_token, 
                        httponly=True, 
                        max_age=timedelta(days=30).total_seconds()
                        )
    
    return SLoginResponse(
        user_id=tokens.user_id,
        access_token=tokens.access_token,
        refresh_token=tokens.refresh_token,
        type="Baerer"
    )

@router.post(
    path="/login/google",
    summary="Авторизация через Google ID токен",
    response_model=SLoginResponse,
    status_code=status.HTTP_200_OK,
)
async def login_with_google(
    data: SLoginRequest,
    response=Response
) -> SLoginResponse:
    service = get_auth_service()
    
    tokens = await service.google_login(data.id_token)

    if tokens is None:
        raise HTTPException(status_code=401, detail="Unable to log in with Google!")
    
    response.set_cookie(key="refresh_token", 
                        value=tokens.refresh_token, 
                        httponly=True, 
                        max_age=timedelta(days=30).total_seconds()
                        )
    
    return SLoginResponse(
        user_id=tokens.user_id,
        access_token=tokens.access_token,
        refresh_token=tokens.refresh_token,
        type="Baerer"
    )