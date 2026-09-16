import os
from pathlib import Path
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+psycopg://postgres:postgres@localhost:5432/civicquest"
    JWT_SECRET: str = "civicquest-dev-secret-key-4a9b-2026-safe-for-local-demo"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    CORS_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000"
    UPLOAD_DIR: str = "uploads"
    DATA_CSV_PATH: str = "data/works_completed.csv"
    
    # Platform rules
    APPROVAL_XP: int = 150
    LEVEL_XP: int = 450
    CERTIFICATE_THRESHOLD: int = 5
    MAX_FILE_SIZE_BYTES: int = 8 * 1024 * 1024  # 8 MB

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @property
    def cors_origin_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

    @property
    def resolved_upload_dir(self) -> Path:
        p = Path(self.UPLOAD_DIR)
        if not p.is_absolute():
            p = BASE_DIR / p
        p.mkdir(parents=True, exist_ok=True)
        return p

    @property
    def resolved_csv_path(self) -> Path:
        p = Path(self.DATA_CSV_PATH)
        if not p.is_absolute():
            p = BASE_DIR / p
        return p

settings = Settings()
