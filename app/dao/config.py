from pydantic import Field
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    PG_HOST: str = Field(validation_alias="POSTGRES_HOST")
    PG_PORT: int = Field(validation_alias="POSTGRES_PORT")

    PG_USER: str = Field(validation_alias="POSTGRES_USER")
    PG_PASSWORD: str = Field(validation_alias="POSTGRES_PASSWORD")

    PG_DB: str = Field(validation_alias="POSTGRES_DB")
    PG_URL: str = ""

    class Config:
        env_file = ".env"


settings = AppSettings()
settings.PG_URL = f'postgresql+psycopg2://{settings.PG_USER}:{settings.PG_PASSWORD}@{settings.PG_HOST}:{settings.PG_PORT}/{settings.PG_DB}'

