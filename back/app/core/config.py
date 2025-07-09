import secrets

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Set model_config for when not using Docker.
    model_config = SettingsConfigDict(
        env_file="../env", 
        env_file_encoding="utf-8",
        extra="ignore"
    )
    
    APP_NAME: str = "API Prueba Tecnica DIVAIN"
    API_V1: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 4 #(4 dias)
    
    POSTGRES_HOST:str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    @property
    def DATABASE_URI(self):
        return (
            f"postgresql+asyncpg://"
            f"{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/"
            f"{self.POSTGRES_DB}"
    )

settings = Settings()