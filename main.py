"""
ProductPilot - 电商图片生成Agent
FastAPI应用入口
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from loguru import logger
import sys

from config.settings import settings
from api.routes import router

# 配置日志
logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
    level=settings.LOG_LEVEL
)

# 创建FastAPI应用
app = FastAPI(
    title="ProductPilot API",
    description="AI驱动的电商图片生成系统",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(router, prefix="/api/v1")


@app.get("/")
async def root():
    """根路径"""
    return {
        "name": "ProductPilot API",
        "version": "1.0.0",
        "description": "AI驱动的电商图片生成系统",
        "docs": "/docs"
    }


@app.on_event("startup")
async def startup_event():
    """应用启动事件"""
    logger.info("=" * 50)
    logger.info("ProductPilot API 启动中...")
    logger.info(f"环境: {settings.APP_ENV}")
    logger.info(f"日志级别: {settings.LOG_LEVEL}")
    logger.info("=" * 50)


@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭事件"""
    logger.info("ProductPilot API 正在关闭...")


if __name__ == "__main__":
    # 运行服务器
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True if settings.APP_ENV == "development" else False,
        log_level=settings.LOG_LEVEL.lower()
    )
