from pydantic import computed_field, PostgresDsn
from pydantic_settings.main import SettingsConfigDict
from secrets import token_urlsafe

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic_core import MultiHostUrl


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_ignore_empty=True)
    
    API_V1_STR: str = '/api/v1'
    ALGORITHM: str = 'HS256'

    SECRET: str = token_urlsafe(32)

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    POSTGRES_SERVER: str = 'localhost'
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = 'postgres'
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "api_db"

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self)-> PostgresDsn:
        return MultiHostUrl.build(
            scheme='postgresql+psycopg',
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            path=self.POSTGRES_DB
        )


settings = Settings()