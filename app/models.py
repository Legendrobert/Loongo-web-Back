from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Table, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

# 用户模型
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    favorites = relationship("Favorite", back_populates="user")

# 城市模型
class City(Base):
    __tablename__ = "cities"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    province = Column(String, index=True)
    region = Column(String, index=True)
    description = Column(Text)
    current_temperature = Column(Float)
    best_season = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    images = relationship("CityImage", back_populates="city", cascade="all, delete-orphan")
    videos = relationship("CityVideo", back_populates="city", cascade="all, delete-orphan")
    pois = relationship("POI", back_populates="city", cascade="all, delete-orphan")
    
# 城市图片模型
class CityImage(Base):
    __tablename__ = "city_images"
    
    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id", ondelete="CASCADE"))
    image_url = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    
    city = relationship("City", back_populates="images")

# 城市视频模型
class CityVideo(Base):
    __tablename__ = "city_videos"
    
    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id", ondelete="CASCADE"))
    video_url = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    
    city = relationship("City", back_populates="videos")

# 兴趣点类型枚举
class POIType:
    ATTRACTION = "attraction"
    RESTAURANT = "restaurant"
    ACCOMMODATION = "accommodation"
    EVENT = "event"

# 兴趣点(Point of Interest)模型
class POI(Base):
    __tablename__ = "pois"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    city_id = Column(Integer, ForeignKey("cities.id", ondelete="CASCADE"))
    poi_type = Column(String)  # 使用POIType的值
    description = Column(Text)
    address = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    city = relationship("City", back_populates="pois")
    images = relationship("POIImage", back_populates="poi", cascade="all, delete-orphan")
    tags = relationship("POITag", back_populates="poi", cascade="all, delete-orphan")

# POI图片模型
class POIImage(Base):
    __tablename__ = "poi_images"
    
    id = Column(Integer, primary_key=True, index=True)
    poi_id = Column(Integer, ForeignKey("pois.id", ondelete="CASCADE"))
    image_url = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    
    poi = relationship("POI", back_populates="images")

# POI标签模型
class POITag(Base):
    __tablename__ = "poi_tags"
    
    id = Column(Integer, primary_key=True, index=True)
    poi_id = Column(Integer, ForeignKey("pois.id", ondelete="CASCADE"))
    tag_name = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    
    poi = relationship("POI", back_populates="tags")

# 收藏模型
class Favorite(Base):
    __tablename__ = "favorites"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    visitor_id = Column(String, nullable=True, index=True)  # 游客ID
    item_id = Column(Integer)  # 可以是城市ID或POI ID
    item_type = Column(String)  # "city" 或 "poi"
    created_at = Column(DateTime, server_default=func.now())
    
    user = relationship("User", back_populates="favorites")