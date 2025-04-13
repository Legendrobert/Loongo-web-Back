from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app import models, schemas, crud
from app.database import engine, get_db
from app.routers import auth, cities, favorites, pois, itinerary

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Loongo Web APP API")

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
    return {"message": "Loongo APP Web API"} 