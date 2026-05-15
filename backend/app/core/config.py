import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Resume Screener"
    API_V1_STR: str = "/api/v1"
    MODEL_NAME: str = os.getenv("MODEL_NAME", "all-MiniLM-L6-v2")

    class Config:
        env_file = ".env"

settings = Settings()
