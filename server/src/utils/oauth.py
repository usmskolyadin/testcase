from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from authlib.integrations.starlette_client import OAuth
from starlette.middleware.sessions import SessionMiddleware
from pydantic import BaseModel
from datetime import datetime, timedelta


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
oauth = OAuth()
oauth.register('google',
    client_id='your_google_client_id',
    client_secret='your_google_client_secret',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'openid email profile'}
)


# Эндпоинт для входа через Google OAuth
@app.get("/login/google")
async def login_google(request):
    redirect_uri = request.url_for('auth_google')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@app.get("/auth/google")
async def auth_google(request):
    token = await oauth.google.authorize_access_token(request)
    user_info = await oauth.google.get('userinfo', token=token)
    email = user_info.json().get('email')
    
    # Здесь можно добавить логику для обработки/сохранения пользователя
    access_token = create_access_token(data={"sub": email})
    return {"access_token": access_token}