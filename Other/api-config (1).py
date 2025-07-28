# config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Self-Building AI"
    API_V1_STR: str = "/api/v1"
    
    # Cloud Services
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str = "us-east-1"
    
    # OpenAI
    OPENAI_API_KEY: str
    
    # Database
    POSTGRES_SERVER: str = "db"
    POSTGRES_USER: str = "admin"
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str = "aibuilder"
    
    class Config:
        case_sensitive = True

settings = Settings()
