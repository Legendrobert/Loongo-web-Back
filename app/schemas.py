from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# 用户相关的模式
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True

# 认证相关模式
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# 城市图片模式
class CityImageBase(BaseModel):
    image_url: str

class CityImage(CityImageBase):
    id: int
    city_id: int

    class Config:
        orm_mode = True

# 城市视频模式
class CityVideoBase(BaseModel):
    video_url: str

class CityVideo(CityVideoBase):
    id: int
    city_id: int

    class Config:
        orm_mode = True

# 城市列表模式
class CityList(BaseModel):
    id: int
    name: str
    province: str
    region: str
    images: List[CityImage]
    videos: List[CityVideo]
    is_favorite: bool = False

    class Config:
        orm_mode = True

# 城市地图模式
class CityMap(BaseModel):
    id: int
    name: str
    latitude: float
    longitude: float
    
    class Config:
        orm_mode = True

# POI图片模式
class POIImageBase(BaseModel):
    image_url: str

class POIImage(POIImageBase):
    id: int
    poi_id: int

    class Config:
        orm_mode = True

# POI标签模式
class POITagBase(BaseModel):
    tag_name: str

class POITag(POITagBase):
    id: int
    poi_id: int

    class Config:
        orm_mode = True

# POI基础模式
class POIBase(BaseModel):
    id: int
    name: str
    poi_type: str
    description: str
    address: str
    latitude: float
    longitude: float
    images: List[POIImage]
    is_favorite: bool = False

    class Config:
        orm_mode = True

# POI地图模式
class POIMap(BaseModel):
    id: int
    name: str
    poi_type: str
    latitude: float
    longitude: float
    is_favorite: bool = False

    class Config:
        orm_mode = True

# POI详情模式
class POIDetail(POIBase):
    tags: List[POITag]
    city_id: int

    class Config:
        orm_mode = True

# 城市详情模式
class CityDetail(CityList):
    description: str
    current_temperature: float
    best_season: str
    latitude: float
    longitude: float
    pois: List[POIBase] = []
    recommended_cities: List[CityList] = []

    class Config:
        orm_mode = True

# 收藏相关模式
class FavoriteResponse(BaseModel):
    is_favorite: bool
    visitor_id: Optional[str] = None

# 收藏的POI模式
class FavoritePOI(POIBase):
    class Config:
        orm_mode = True

# 收藏的城市模式
class FavoriteCity(BaseModel):
    id: int
    name: str
    province: str
    images: List[CityImage]
    pois: List[FavoritePOI] = []
    poi_count: int = 0

    class Config:
        orm_mode = True 