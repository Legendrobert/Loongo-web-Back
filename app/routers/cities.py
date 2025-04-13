from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app import crud, models, schemas
from app.database import get_db
from app.routers.auth import get_optional_current_user

router = APIRouter(
    prefix="/cities",
    tags=["城市"],
)

@router.get("/", response_model=List[schemas.CityList])
def get_cities_by_region(
    region: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Optional[models.User] = Depends(get_optional_current_user)
):
    """
    获取城市列表
    
    按照区域划分城市列表，返回城市头图及视频、城市名称、所属省份、收藏状态
    """
    cities = crud.get_cities(db, region=region, skip=skip, limit=limit)
    
    # 检查收藏状态
    user_id = None if current_user is None else current_user.id
    for city in cities:
        city.is_favorite = crud.check_favorite(db, user_id=user_id, item_id=city.id, item_type="city")
    
    return cities

@router.get("/map", response_model=List[schemas.CityMap])
def get_cities_map_data(
    db: Session = Depends(get_db),
    current_user: Optional[models.User] = Depends(get_optional_current_user)
):
    """
    获取地图模式城市数据
    
    返回所有城市的地理位置信息，用于地图模式展示
    """
    return crud.get_cities_map_data(db)

@router.get("/search", response_model=List[schemas.CityList])
def search_cities(
    query: str,
    db: Session = Depends(get_db),
    current_user: Optional[models.User] = Depends(get_optional_current_user)
):
    """
    搜索城市
    
    模糊搜索城市、省份名称，展示对应搜索结果
    """
    cities = crud.search_cities(db, query=query)
    
    # 检查收藏状态
    user_id = None if current_user is None else current_user.id
    for city in cities:
        city.is_favorite = crud.check_favorite(db, user_id=user_id, item_id=city.id, item_type="city")
    
    return cities

@router.get("/{city_id}", response_model=schemas.CityDetail)
def get_city_detail(
    city_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[models.User] = Depends(get_optional_current_user)
):
    """
    获取城市详情
    
    返回城市图片及视频、城市简介、当前温度、适宜季节、推荐旅游项目、美食、住宿、社媒视频和标签等
    """
    city = crud.get_city(db, city_id=city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="城市不存在")
    
    # 检查收藏状态
    user_id = None if current_user is None else current_user.id
    city.is_favorite = crud.check_favorite(db, user_id=user_id, item_id=city.id, item_type="city")
    
    # 获取相关城市推荐
    city.recommended_cities = crud.get_recommended_cities(db, city_id=city_id)
    
    return city

@router.get("/{city_id}/map", response_model=List[schemas.POIMap])
def get_city_map_data(
    city_id: int,
    poi_type: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Optional[models.User] = Depends(get_optional_current_user)
):
    """
    获取城市地图模式数据
    
    返回城市内的点位信息，用于地图模式展示
    """
    city = crud.get_city(db, city_id=city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="城市不存在")
    
    pois = crud.get_city_pois_map_data(db, city_id=city_id, poi_type=poi_type)
    
    # 检查收藏状态
    user_id = None if current_user is None else current_user.id
    for poi in pois:
        poi.is_favorite = crud.check_favorite(db, user_id=user_id, item_id=poi.id, item_type="poi")
    
    return pois

@router.get("/{city_id}/search", response_model=List[schemas.POIBase])
def search_city_pois(
    city_id: int,
    query: str,
    db: Session = Depends(get_db),
    current_user: Optional[models.User] = Depends(get_optional_current_user)
):
    """
    搜索城市内点位
    
    在指定城市内搜索点位信息
    """
    city = crud.get_city(db, city_id=city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="城市不存在")
    
    pois = crud.search_city_pois(db, city_id=city_id, query=query)
    
    # 检查收藏状态
    user_id = None if current_user is None else current_user.id
    for poi in pois:
        poi.is_favorite = crud.check_favorite(db, user_id=user_id, item_id=poi.id, item_type="poi")
    
    return pois 