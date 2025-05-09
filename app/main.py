from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app import models
from app.database import engine, get_db
from app.config import settings
from app.routers import auth, cities, favorites, pois, itinerary

# 创建数据库表
models.Base.metadata.create_all(bind=engine)

# 创建FastAPI应用实例
app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 引入路由模块
app.include_router(auth.router)
app.include_router(cities.router)
app.include_router(favorites.router)
app.include_router(pois.router)
app.include_router(itinerary.router)

@app.get("/")
def read_root():
    """API根路径的欢迎信息"""
    return {"message": settings.APP_NAME} 

# 为新系统添加健康检查端点
@app.get("/health")
def health_check():
    """系统健康检查端点"""
    return {
        "status": "healthy",
        "version": "1.0.0"
    }