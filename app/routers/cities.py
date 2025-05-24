from fastapi import APIRouter, Depends, HTTPException, Query, Cookie
from sqlalchemy.orm import Session
from typing import List, Optional

import crud, models, schemas
from database import get_db
from routers.auth import get_optional_current_user
from utils.cities_utils import get_ai_city_details, get_bing_image_urls, get_popular_events_for_city, get_featured_restaurants_for_city, get_cozy_hotels_for_city, get_expert_opinions_for_city

router = APIRouter(
    prefix="/cities",
    tags=["城市"],
)

@router.get("/", response_model=List[schemas.CityList])
async def get_cities_by_region(
    region: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Optional[models.User] = Depends(get_optional_current_user),
    visitor_id: Optional[str] = Cookie(None)
):
    """
    获取城市列表
    
    按照区域划分城市列表，返回城市头图及视频、城市名称、所属省份、收藏状态
    """
    cities = crud.get_cities(db, region=region, skip=skip, limit=limit)
    
    # 检查收藏状态
    user_id = current_user.id if current_user else None
    for city in cities:
        city.is_favorite = crud.check_favorite(
            db, 
            item_id=city.id, 
            item_type="city",
            user_id=user_id,
            visitor_id=visitor_id if not user_id else None
        )
    
    return cities

@router.get("/map", response_model=List[schemas.CityMap])
async def get_cities_map_data(db: Session = Depends(get_db)):
    """
    获取地图模式城市数据
    
    返回所有城市的地理位置信息，用于地图模式展示
    """
    return crud.get_cities_map_data(db)

@router.get("/search", response_model=List[schemas.CityList])
async def search_cities(
    query: str,
    db: Session = Depends(get_db),
    current_user: Optional[models.User] = Depends(get_optional_current_user),
    visitor_id: Optional[str] = Cookie(None)
):
    """
    搜索城市
    
    模糊搜索城市、省份名称，展示对应搜索结果
    """
    cities = crud.search_cities(db, query=query)
    
    # 检查收藏状态
    user_id = current_user.id if current_user else None
    for city in cities:
        city.is_favorite = crud.check_favorite(
            db, 
            item_id=city.id, 
            item_type="city",
            user_id=user_id,
            visitor_id=visitor_id if not user_id else None
        )
    
    return cities

@router.get("/{city_id}", response_model=schemas.CityDetail)
async def get_city_detail(
    city_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[models.User] = Depends(get_optional_current_user),
    visitor_id: Optional[str] = Cookie(None)
):
    """
    获取城市详情
    
    返回城市图片及视频、城市简介、当前温度、适宜季节、推荐旅游项目、美食、住宿等
    """
    # 获取城市信息
    city = crud.get_city(db, city_id=city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="城市不存在")
    
    # 检查城市收藏状态
    user_id = current_user.id if current_user else None
    city.is_favorite = crud.check_favorite(
        db, 
        item_id=city.id, 
        item_type="city",
        user_id=user_id,
        visitor_id=visitor_id if not user_id else None
    )
    
    # 检查POI收藏状态
    for poi in city.pois:
        poi.is_favorite = crud.check_favorite(
            db, 
            item_id=poi.id, 
            item_type="poi",
            user_id=user_id,
            visitor_id=visitor_id if not user_id else None
        )
    
    # 获取相关城市推荐
    recommended_cities = crud.get_recommended_cities(db, city_id=city_id)
    
    # 检查推荐城市收藏状态
    for rec_city in recommended_cities:
        rec_city.is_favorite = crud.check_favorite(
            db, 
            item_id=rec_city.id, 
            item_type="city",
            user_id=user_id,
            visitor_id=visitor_id if not user_id else None
        )
    
    city.recommended_cities = recommended_cities
    
    # 获取AI生成的城市详情信息
    ai_details = get_ai_city_details(city.name)
    city.suggested_visit_time = ai_details.get("suggested_visit_time", "")
    city.activity_suggestions = ai_details.get("activity_suggestions", "")
    city.site_description = ai_details.get("site_description", "")
    
    # 获取额外图片
    city.additional_images = get_bing_image_urls(f"{city.name} city scenery", count=5)
    
    city.popular_events = get_popular_events_for_city(db, city_id)
    city.featured_restaurants = get_featured_restaurants_for_city(db, city_id)
    city.cozy_hotels = get_cozy_hotels_for_city(db, city_id)
    city.expert_opinions = get_expert_opinions_for_city(db, city_id)
    
    return city

@router.get("/{city_id}/map", response_model=List[schemas.POIMap])
async def get_city_map_data(
    city_id: int,
    poi_type: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Optional[models.User] = Depends(get_optional_current_user),
    visitor_id: Optional[str] = Cookie(None)
):
    """
    获取城市地图模式数据
    
    返回城市内的点位信息，用于地图模式展示
    """
    # 检查城市是否存在
    city = crud.get_city(db, city_id=city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="城市不存在")
    
    # 获取城市POI数据
    pois = crud.get_city_pois_map_data(db, city_id=city_id, poi_type=poi_type)
    
    # 检查收藏状态
    user_id = current_user.id if current_user else None
    for poi in pois:
        poi.is_favorite = crud.check_favorite(
            db, 
            item_id=poi.id, 
            item_type="poi",
            user_id=user_id,
            visitor_id=visitor_id if not user_id else None
        )
    
    return pois

@router.get("/{city_id}/search", response_model=List[schemas.POIBase])
async def search_city_pois(
    city_id: int,
    query: str,
    db: Session = Depends(get_db),
    current_user: Optional[models.User] = Depends(get_optional_current_user),
    visitor_id: Optional[str] = Cookie(None)
):
    """
    搜索城市内点位
    
    在指定城市内搜索点位信息
    """
    # 检查城市是否存在
    city = crud.get_city(db, city_id=city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="城市不存在")
    
    # 搜索城市POI
    pois = crud.search_city_pois(db, city_id=city_id, query=query)
    
    # 检查收藏状态
    user_id = current_user.id if current_user else None
    for poi in pois:
        poi.is_favorite = crud.check_favorite(
            db, 
            item_id=poi.id, 
            item_type="poi",
            user_id=user_id,
            visitor_id=visitor_id if not user_id else None
        )
    
    return pois