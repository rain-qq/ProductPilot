"""
应用配置管理
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """应用配置"""
    
    # API Keys
    OPENAI_API_KEY: str
    OPENAI_API_BASE: str = "https://api.openai.com/v1"
    ANTHROPIC_API_KEY: Optional[str] = None
    
    # Stable Diffusion
    SD_WEBUI_URL: str = "http://localhost:7860"
    
    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    
    # MinIO Storage
    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_BUCKET_NAME: str = "ecommerce-images"
    
    # Application
    APP_ENV: str = "development"
    LOG_LEVEL: str = "INFO"
    MAX_IMAGE_GENERATION_RETRIES: int = 3
    QUALITY_THRESHOLD: float = 0.8
    
    # Image Generation Defaults
    DEFAULT_IMAGE_WIDTH: int = 1024
    DEFAULT_IMAGE_HEIGHT: int = 1024
    DEFAULT_BATCH_SIZE: int = 4
    DEFAULT_STEPS: int = 30
    DEFAULT_CFG_SCALE: float = 7.5
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# 全局配置实例
settings = Settings()
