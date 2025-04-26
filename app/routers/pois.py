from fastapi import APIRouter, Depends, HTTPException, Cookie
from sqlalchemy.orm import Session
from typing import Optional

import crud, models, schemas
from database import get_db
from routers.auth import get_optional_current_user

router = APIRouter(
    prefix="/pois",
    tags=["兴趣点"],
)

@router.get("/{poi_id}", response_model=schemas.POIDetail)
async def get_poi_detail(
    poi_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[models.User] = Depends(get_optional_current_user),
    visitor_id: Optional[str] = Cookie(None)
):
    """
    获取兴趣点详情
    
    返回兴趣点的详细信息，包括名称、描述、地址、图片等
    """
    poi = crud.get_poi_detail(db, poi_id=poi_id)
    if poi is None:
        raise HTTPException(status_code=404, detail="兴趣点不存在")
    
    # 检查收藏状态
    user_id = current_user.id if current_user else None
    poi.is_favorite = crud.check_favorite(
        db, 
        item_id=poi.id, 
        item_type="poi",
        user_id=user_id,
        visitor_id=visitor_id if not user_id else None
    )
    
    return poi