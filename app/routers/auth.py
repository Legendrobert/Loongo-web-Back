from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional
import uuid

from config import settings
from database import get_db
from utils.security import create_access_token
import models, schemas, crud

router = APIRouter(
    prefix="/auth",
    tags=["认证"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token", auto_error=False)

async def get_current_user(token: Optional[str] = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """获取当前登录用户，验证失败抛出401错误"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无效的认证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    if token is None:
        raise credentials_exception
        
    try:
        # 解码JWT令牌
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        
        # 获取用户名
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
            
        # 创建令牌数据对象
        token_data = schemas.TokenData(username=username, exp=payload.get("exp"))
    except JWTError:
        raise credentials_exception
        
    # 查询用户
    user = crud.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
        
    return user

async def get_optional_current_user(token: Optional[str] = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """获取当前用户，如果未登录则返回None"""
    if token is None:
        return None
        
    try:
        return await get_current_user(token, db)
    except HTTPException:
        return None

@router.post("/register", response_model=schemas.User)
async def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    注册新用户
    
    接收用户名、电子邮件和密码，创建新用户账号并存储在数据库中
    """
    # 检查邮箱是否已注册
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="邮箱已被注册"
        )
    
    # 检查用户名是否已注册
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已被注册"
        )
    
    # 创建新用户
    return crud.create_user(db=db, user=user)

@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db),
    visitor_id: Optional[str] = Cookie(None)
):
    """
    用户登录并获取访问令牌
    
    验证用户凭据，如果有效则返回JWT令牌
    """
    # 验证用户凭据
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 合并游客收藏（如果存在）
    if visitor_id:
        crud.merge_visitor_favorites(db, user_id=user.id, visitor_id=visitor_id)
    
    # 创建访问令牌
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    
    # 返回令牌信息
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }

@router.get("/me", response_model=schemas.User)
async def read_users_me(current_user: models.User = Depends(get_current_user)):
    """获取当前登录用户信息"""
    return current_user