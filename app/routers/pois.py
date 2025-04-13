from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from app import crud, models, schemas
from app.database import get_db
from app.routers.auth import get_optional_current_user

router = APIRouter(
    prefix="/pois",
    tags=["兴趣点"],
)

@router.get("/{poi_id}", response_model=schemas.POIDetail)
def get_poi_detail(
    poi_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[models.User] = Depends(get_optional_current_user)
):
    """
    获取兴趣点详情
    
    返回兴趣点的详细信息，包括名称、描述、地址、图片等
    """
    poi = crud.get_poi_detail(db, poi_id=poi_id)
    if poi is None:
        raise HTTPException(status_code=404, detail="兴趣点不存在")
    
    # 检查收藏状态
    user_id = None if current_user is None else current_user.id
    poi.is_favorite = crud.check_favorite(db, user_id=user_id, item_id=poi.id, item_type="poi")
    
    return poi 