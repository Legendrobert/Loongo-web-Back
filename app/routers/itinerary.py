from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app import crud, models, schemas
from app.database import get_db
from app.routers.auth import get_current_user, get_optional_current_user

router = APIRouter(
    prefix="/itinerary",
    tags=["行程"],
)

@router.get("/favorites", response_model=List[schemas.FavoriteCity])
def get_favorite_cities(
    db: Session = Depends(get_db),
    current_user: Optional[models.User] = Depends(get_optional_current_user)
):
    """
    获取收藏页面
    
    展示用户收藏了哪些内容，以城市为卡片，具体收藏点位放在卡片内
    用户浏览过的城市但没有收藏具体点位也会作为卡片展示
    收藏点位会统计总数，展示在城市卡片上
    """
    if current_user is None:
        raise HTTPException(status_code=401, detail="需要登录")
    
    return crud.get_user_favorites(db, user_id=current_user.id) 