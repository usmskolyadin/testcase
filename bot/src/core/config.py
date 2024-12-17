from pydantic import Field, EmailStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_url: str = Field(default='http://127.0.0.1:8000/api/v1', alias='API_URL')
    telegram_api_key: str = Field(default='', alias='TELEGRAM_API_KEY')

    class Config:
        env_file = ".env"  

settings = Settings()
