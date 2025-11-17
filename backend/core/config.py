from pydantic_settings import BaseSettings
from typing import List
from pathlib import Path


def get_env_file():
    """Get .env file path with fallback to .env.development or .env.production"""
    backend_dir = Path(__file__).parent.parent
    
    env_files = [
        backend_dir / ".env",
        backend_dir / ".env.development",
        backend_dir / ".env.production"
    ]
    
    for env_file in env_files:
        if env_file.exists():
            return str(env_file)
    
    return None


class Settings(BaseSettings):
    BASE_URL: str = "http://localhost:8000"
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_NAME: str = "repair"
    DB_USER: str = "root"
    DB_PASSWORD: str = ""
    JWT_SECRET_KEY: str = "your-super-secret-jwt-key-change-this-in-production-12345678"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24
    ACCESS_TOKEN_EXPIRE_HOURS: int = 24
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    @property
    def JWT_SECRET(self) -> str:
        return self.JWT_SECRET_KEY

    @property
    def database_url(self) -> str:
        return f"mysql+aiomysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?charset=utf8mb4"
    
    @property
    def database_url_sync(self) -> str:
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?charset=utf8mb4"

    class Config:
        env_file = get_env_file()
        case_sensitive = True


settings = Settings()

