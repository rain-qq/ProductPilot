"""
应用配置管理
"""
from pydantic_settings import BaseSettings
from typing import Optional, Dict, Any


class Settings(BaseSettings):
    """应用配置"""

    # API Keys
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_API_BASE: str = "https://api.openai.com/v1"
    OPENAI_MODEL: str = "gpt-4"
    GOOGLE_API_KEY: Optional[str] = None
    GEMINI_MODEL: str = "gemini-pro"
    GEMINI_IMAGE_MODEL: str = "gemini-2.5-flash-image"  # 专门用于图片生成的Gemini模型
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

    # 电商平台预设配置
    PLATFORM_PRESETS: Dict[str, Dict[str, Any]] = {
        "amazon": {
            "background": "pure_white",
            "product_coverage": 0.85,
            "min_resolution": (1000, 1000),
            "format": "jpeg",
            "allow_text": False,
            "allow_watermark": False,
            "allow_border": False,
            "negative_prompt": "text, watermark, logo, border, frame, shadow, reflection, low quality, blurry",
            "style_keywords": "professional product photography, studio lighting, clean composition, commercial grade",
            "quality_threshold": 0.85
        },
        "temu": {
            "background": "white_or_scene",
            "product_coverage": 0.7,
            "min_resolution": (800, 800),
            "format": "png",
            "allow_text": False,
            "allow_watermark": False,
            "allow_border": True,
            "negative_prompt": "low quality, blurry, pixelated, distorted",
            "style_keywords": "high definition, lifestyle scene, vibrant colors, clear details",
            "quality_threshold": 0.75
        },
        "default": {
            "background": "any",
            "product_coverage": 0.6,
            "min_resolution": (800, 800),
            "format": "png",
            "allow_text": False,
            "allow_watermark": False,
            "allow_border": True,
            "negative_prompt": "low quality, blurry",
            "style_keywords": "professional, high quality",
            "quality_threshold": 0.8
        }
    }

    class Config:
        env_file = ".env"
        case_sensitive = True


# 全局配置实例
settings = Settings()
