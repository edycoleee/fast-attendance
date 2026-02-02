"""
Application Settings and Configuration
"""
import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    """Application settings from environment variables"""
    
    # Application
    APP_NAME: str = "RSUD Sulfat Attendance System"
    APP_VERSION: str = "2.0.0"
    APP_DESCRIPTION: str = "Sistem Attendance RSUD Sulfat - PostgreSQL"
    
    # Database
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "attendance_db")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "sultan")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "Sulfat123#!")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "12.50.20.250")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    
    @property
    def DATABASE_URL(self) -> str:
        """Construct SQLAlchemy database URL"""
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    @property
    def DB_CONFIG(self) -> dict:
        """Database configuration for psycopg2"""
        return {
            'dbname': self.POSTGRES_DB,
            'user': self.POSTGRES_USER,
            'password': self.POSTGRES_PASSWORD,
            'host': self.POSTGRES_HOST,
            'port': self.POSTGRES_PORT
        }
    
    class Config:
        case_sensitive = True


# Global settings instance
settings = Settings()
