from urllib.parse import quote_plus
from pydantic import computed_field, PostgresDsn
from pydantic_settings.main import SettingsConfigDict
from pydantic_settings import BaseSettings, SettingsConfigDict
from secrets import token_urlsafe


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='./.env',
        env_ignore_empty=True,
        extra='ignore')
    
    API_V1_STR: str = '/api/v1'
    ALGORITHM: str = 'HS256'

    SECRET: str = token_urlsafe(32)

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    POSTGRES_SERVER: str = 'localhost'
    POSTGRES_PORT: int  = 5432
    POSTGRES_USER: str = 'postgres'
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "api"

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self)-> PostgresDsn:
        return PostgresDsn.build(
            scheme='postgresql+psycopg',
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            username=self.POSTGRES_USER,
            password=quote_plus(self.POSTGRES_PASSWORD),
            path=self.POSTGRES_DB
        )


settings = Settings()