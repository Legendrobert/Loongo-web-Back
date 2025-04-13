from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from datetime import datetime, timedelta
from jose import jwt
from typing import Optional, List
import uuid

from app.utils.security import get_password_hash, verify_password
from app import models, schemas

# 用户相关操作
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, secret_key: str = "YOUR_SECRET_KEY", algorithm: str = "HS256", expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt

# 城市相关操作
def get_cities(db: Session, region: Optional[str] = None, skip: int = 0, limit: int = 100):
    query = db.query(models.City)
    if region:
        query = query.filter(models.City.region == region)
    return query.offset(skip).limit(limit).all()

def get_city(db: Session, city_id: int):
    return db.query(models.City).filter(models.City.id == city_id).first()

def get_cities_map_data(db: Session):
    return db.query(models.City).all()

def search_cities(db: Session, query: str):
    search = f"%{query}%"
    return db.query(models.City).filter(
        or_(
            models.City.name.like(search),
            models.City.province.like(search)
        )
    ).all()

def get_recommended_cities(db: Session, city_id: int, limit: int = 5):
    city = get_city(db, city_id)
    if not city:
        return []
    
    # 获取相关城市（这里简化为获取相同区域的其他城市）
    return db.query(models.City).filter(
        and_(
            models.City.region == city.region,
            models.City.id != city_id
        )
    ).limit(limit).all()

# POI相关操作
def get_poi(db: Session, poi_id: int):
    return db.query(models.POI).filter(models.POI.id == poi_id).first()

def get_poi_detail(db: Session, poi_id: int):
    return db.query(models.POI).filter(models.POI.id == poi_id).first()

def get_city_pois_map_data(db: Session, city_id: int, poi_type: Optional[str] = None):
    query = db.query(models.POI).filter(models.POI.city_id == city_id)
    if poi_type:
        query = query.filter(models.POI.poi_type == poi_type)
    return query.all()

def search_city_pois(db: Session, city_id: int, query: str):
    search = f"%{query}%"
    return db.query(models.POI).filter(
        and_(
            models.POI.city_id == city_id,
            models.POI.name.like(search)
        )
    ).all()

# 收藏相关操作
def check_favorite(db: Session, user_id: Optional[int], item_id: int, item_type: str, visitor_id: Optional[str] = None):
    if user_id:
        favorite = db.query(models.Favorite).filter(
            and_(
                models.Favorite.user_id == user_id,
                models.Favorite.item_id == item_id,
                models.Favorite.item_type == item_type
            )
        ).first()
        return favorite is not None
    elif visitor_id:
        # 游客收藏存储在另一个表或使用visitor_id字段
        favorite = db.query(models.Favorite).filter(
            and_(
                models.Favorite.visitor_id == visitor_id,
                models.Favorite.item_id == item_id,
                models.Favorite.item_type == item_type
            )
        ).first()
        return favorite is not None
    return False

def toggle_favorite(db: Session, item_id: int, item_type: str, user_id: Optional[int] = None, visitor_id: Optional[str] = None):
    if user_id:
        # 用户已登录
        favorite = db.query(models.Favorite).filter(
            and_(
                models.Favorite.user_id == user_id,
                models.Favorite.item_id == item_id,
                models.Favorite.item_type == item_type
            )
        ).first()
        
        if favorite:
            # 取消收藏
            db.delete(favorite)
            db.commit()
            return False
        else:
            # 添加收藏
            db_favorite = models.Favorite(
                user_id=user_id,
                item_id=item_id,
                item_type=item_type
            )
            db.add(db_favorite)
            db.commit()
            return True
    elif visitor_id:
        # 游客收藏
        favorite = db.query(models.Favorite).filter(
            and_(
                models.Favorite.visitor_id == visitor_id,
                models.Favorite.item_id == item_id,
                models.Favorite.item_type == item_type
            )
        ).first()
        
        if favorite:
            # 取消收藏
            db.delete(favorite)
            db.commit()
            return False
        else:
            # 添加收藏
            db_favorite = models.Favorite(
                visitor_id=visitor_id,
                item_id=item_id,
                item_type=item_type
            )
            db.add(db_favorite)
            db.commit()
            return True
    
    return False

def merge_visitor_favorites(db: Session, user_id: int, visitor_id: str):
    # 获取游客的所有收藏
    visitor_favorites = db.query(models.Favorite).filter(models.Favorite.visitor_id == visitor_id).all()
    
    for favorite in visitor_favorites:
        # 检查用户是否已经收藏了这个项目
        existing_favorite = db.query(models.Favorite).filter(
            and_(
                models.Favorite.user_id == user_id,
                models.Favorite.item_id == favorite.item_id,
                models.Favorite.item_type == favorite.item_type
            )
        ).first()
        
        if not existing_favorite:
            # 将收藏转移到用户名下
            favorite.user_id = user_id
            favorite.visitor_id = None
    
    db.commit()

def get_user_favorites(db: Session, user_id: int):
    # 获取用户收藏的城市
    city_favorites = db.query(models.Favorite).filter(
        and_(
            models.Favorite.user_id == user_id,
            models.Favorite.item_type == "city"
        )
    ).all()
    
    favorite_cities = []
    for favorite in city_favorites:
        city = db.query(models.City).filter(models.City.id == favorite.item_id).first()
        if city:
            # 获取该城市下收藏的POI
            poi_favorites = db.query(models.Favorite).filter(
                and_(
                    models.Favorite.user_id == user_id,
                    models.Favorite.item_type == "poi"
                )
            ).join(
                models.POI, 
                and_(models.Favorite.item_id == models.POI.id, models.POI.city_id == city.id)
            ).all()
            
            pois = []
            for poi_favorite in poi_favorites:
                poi = db.query(models.POI).filter(models.POI.id == poi_favorite.item_id).first()
                if poi:
                    pois.append(poi)
            
            city.pois = pois
            city.poi_count = len(pois)
            favorite_cities.append(city)
    
    return favorite_cities

def get_visitor_favorites(db: Session, visitor_id: str):
    # 获取游客收藏的城市
    city_favorites = db.query(models.Favorite).filter(
        and_(
            models.Favorite.visitor_id == visitor_id,
            models.Favorite.item_type == "city"
        )
    ).all()
    
    favorite_cities = []
    for favorite in city_favorites:
        city = db.query(models.City).filter(models.City.id == favorite.item_id).first()
        if city:
            # 获取该城市下收藏的POI
            poi_favorites = db.query(models.Favorite).filter(
                and_(
                    models.Favorite.visitor_id == visitor_id,
                    models.Favorite.item_type == "poi"
                )
            ).join(
                models.POI, 
                and_(models.Favorite.item_id == models.POI.id, models.POI.city_id == city.id)
            ).all()
            
            pois = []
            for poi_favorite in poi_favorites:
                poi = db.query(models.POI).filter(models.POI.id == poi_favorite.item_id).first()
                if poi:
                    pois.append(poi)
            
            city.pois = pois
            city.poi_count = len(pois)
            favorite_cities.append(city)
    
    return favorite_cities 