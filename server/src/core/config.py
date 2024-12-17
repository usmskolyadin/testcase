from pydantic import Field, EmailStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_host: str = Field(default='localhost', alias='DB_HOST')
    db_port: int = Field(default=5432, alias='DB_PORT')
    db_name: str = Field(default='postgres', alias='DB_NAME')
    db_user: str = Field(default='postgres', alias='DB_USER')
    db_pass: str = Field(default='postgres', alias='DB_PASS')

    mongo_host: str = Field(default="localhost", alias="MONGO_HOST")
    mongo_port: int = Field(default=27017, alias="MONGO_PORT")

    redis_host: str = Field(default='localhost', alias='REDIS_HOST')
    redis_port: int = Field(default=6379, alias='REDIS_PORT')
    redis_pass: str = Field(default='qwerty', alias='REDIS_PASS')

    echo: bool = True
    
    jwt_access_token_expire_minutes: int = Field(default=15)
    jwt_refresh_token_expire_minutes: int = Field(default=44640)
    jwt_secret_key: str = Field(default='', alias='JWT_SECRET_KEY')
    jwt_algorithm: str = Field(default='HS256', alias='JWT_ALGORITHM')

    @property
    def db_url(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"

    @property
    def mongodb_url(self) -> str:
        return f"mongodb://localhost:{27017}"


settings = Settings()
