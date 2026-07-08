from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    PROJECT_NAME: str = "AGENT-API"
    VERSION: str = "1.0.0"
    ENVIRONMENT: Literal["development", "testing", "production"] = "development"
    DATABASE_URL: str = "sqlite:///database.db"
    SECRET_KEY: str = "super-secret-default-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    OPENAI_API_KEY: str
    
    model_config = SettingsConfigDict(
        env_file=".env",            
        env_file_encoding="utf-8",  
        extra="ignore"              
    )

settings = Settings()