from pydantic_settings import BaseSettings
from typing import List
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Settings(BaseSettings):
    # 应用配置
    APP_NAME: str = "Loongo Web APP API"
    DEBUG: bool = True
    
    # 认证配置
    SECRET_KEY: str = os.getenv("SECRET_KEY", "Loongo@2025")  # 默认为开发密钥，生产环境应使用环境变量
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # 数据库配置
    DATABASE_URL: str = "sqlite:///./app.db"
    
    # CORS配置
    CORS_ORIGINS: List[str] = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# 创建设置实例
settings = Settings()