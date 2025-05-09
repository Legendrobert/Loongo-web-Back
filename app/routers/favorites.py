from fastapi import APIRouter, Depends, HTTPException, Cookie, Response
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid

from app import crud, models, schemas
from app.database import get_db
from app.routers.auth import get_optional_current_user

router = APIRouter(
    prefix="/favorites",
    tags=["收藏"],
)

@router.post("/city/{city_id}", response_model=schemas.FavoriteResponse)
async def toggle_favorite_city(
    city_id: int,
    response: Response,
    db: Session = Depends(get_db),
    current_user: Optional[models.User] = Depends(get_optional_current_user),
    visitor_id: Optional[str] = Cookie(None)
):
    """
    收藏/取消收藏城市
    
    用户未登录时收藏到游客态收藏夹，用户登录后游客态收藏加入到账号下
    已登录用户点击已收藏可取消收藏
    """
    # 检查城市是否存在
    city = crud.get_city(db, city_id=city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="城市不存在")
    
    if current_user:
        # 已登录用户
        user_id = current_user.id
        
        # 如果存在visitor_id，合并游客收藏
        if visitor_id:
            crud.merge_visitor_favorites(db, user_id=user_id, visitor_id=visitor_id)
        
        is_favorite = crud.toggle_favorite(db, user_id=user_id, item_id=city_id, item_type="city")
        return {"is_favorite": is_favorite}
    else:
        # 游客模式
        if not visitor_id:
            visitor_id = str(uuid.uuid4())
            # 设置cookie
            response.set_cookie(key="visitor_id", value=visitor_id, httponly=True, max_age=60*60*24*30)  # 30天
        
        is_favorite = crud.toggle_favorite(db, visitor_id=visitor_id, item_id=city_id, item_type="city")
        return {"is_favorite": is_favorite, "visitor_id": visitor_id}

@router.post("/poi/{poi_id}", response_model=schemas.FavoriteResponse)
async def toggle_favorite_poi(
    poi_id: int,
    response: Response,
    db: Session = Depends(get_db),
    current_user: Optional[models.User] = Depends(get_optional_current_user),
    visitor_id: Optional[str] = Cookie(None)
):
    """
    收藏/取消收藏兴趣点
    
    用户未登录时收藏到游客态收藏夹，用户登录后游客态收藏加入到账号下
    已登录用户点击已收藏可取消收藏
    """
    # 检查POI是否存在
    poi = crud.get_poi(db, poi_id=poi_id)
    if poi is None:
        raise HTTPException(status_code=404, detail="兴趣点不存在")
    
    if current_user:
        # 已登录用户
        user_id = current_user.id
        
        # 如果存在visitor_id，合并游客收藏
        if visitor_id:
            crud.merge_visitor_favorites(db, user_id=user_id, visitor_id=visitor_id)
        
        is_favorite = crud.toggle_favorite(db, user_id=user_id, item_id=poi_id, item_type="poi")
        return {"is_favorite": is_favorite}
    else:
        # 游客模式
        if not visitor_id:
            visitor_id = str(uuid.uuid4())
            # 设置cookie
            response.set_cookie(key="visitor_id", value=visitor_id, httponly=True, max_age=60*60*24*30)  # 30天
        
        is_favorite = crud.toggle_favorite(db, visitor_id=visitor_id, item_id=poi_id, item_type="poi")
        return {"is_favorite": is_favorite, "visitor_id": visitor_id}

@router.get("/", response_model=List[schemas.FavoriteCity])
async def get_favorites(
    db: Session = Depends(get_db),
    current_user: Optional[models.User] = Depends(get_optional_current_user),
    visitor_id: Optional[str] = Cookie(None)
):
    """
    获取收藏列表
    
    展示用户收藏的内容，以城市为卡片，具体收藏点位放在卡片内
    用户浏览过的城市但没有收藏具体点位也会作为卡片展示
    """
    if current_user:
        # 已登录用户
        user_id = current_user.id
        
        # 如果存在visitor_id，合并游客收藏
        if visitor_id:
            crud.merge_visitor_favorites(db, user_id=user_id, visitor_id=visitor_id)
        
        return crud.get_user_favorites(db, user_id=user_id)
    elif visitor_id:
        # 游客模式
        return crud.get_visitor_favorites(db, visitor_id=visitor_id)
    else:
        # 没有游客ID
        return []