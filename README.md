# Loongo-web-Back

## 功能实现对应关系

### 用户认证模块 (app/routers/auth.py)

| 功能 | API端点 | 描述 |
|------|---------|------|
| 用户注册 | POST /auth/register | 创建新用户账号 |
| 用户登录 | POST /auth/token | 获取访问令牌 |

### 城市浏览模块 (app/routers/cities.py)

| 功能 | API端点 | 描述 |
|------|---------|------|
| 城市列表 | GET /cities/ | 按照区域划分城市列表，返回城市信息和收藏状态 |
| 地图模式 | GET /cities/map | 返回所有城市的地理位置信息，用于地图模式展示 |
| 城市搜索 | GET /cities/search | 模糊搜索城市、省份名称，展示搜索结果 |
| 城市详情 | GET /cities/{city_id} | 返回城市详细信息，包括城市图片、视频、简介等 |
| 城市地图模式 | GET /cities/{city_id}/map | 返回城市内的点位信息，用于地图模式展示 |
| 城市内搜索 | GET /cities/{city_id}/search | 在指定城市内搜索点位信息 |

### 收藏功能模块 (app/routers/favorites.py)

| 功能 | API端点 | 描述 |
|------|---------|------|
| 收藏/取消收藏城市 | POST /favorites/city/{city_id} | 切换城市收藏状态，支持游客收藏 |
| 收藏/取消收藏兴趣点 | POST /favorites/poi/{poi_id} | 切换兴趣点收藏状态，支持游客收藏 |
| 获取收藏列表 | GET /favorites/ | 获取用户或游客的收藏列表 |

### 兴趣点模块 (app/routers/pois.py)

| 功能 | API端点 | 描述 |
|------|---------|------|
| 兴趣点详情 | GET /pois/{poi_id} | 获取兴趣点详细信息 |

### 行程模块 (app/routers/itinerary.py)

| 功能 | API端点 | 描述 |
|------|---------|------|
| 收藏页面 | GET /itinerary/favorites | 展示用户收藏的城市和点位 |

## 数据模型

### 用户 (User)
- 用户名、邮箱、密码哈希、活跃状态
- 关联收藏记录

### 城市 (City)
- 城市名称、省份、区域、描述、温度、最佳季节、地理坐标
- 关联图片、视频、兴趣点

### 兴趣点 (POI)
- 名称、类型(景点/餐厅/住宿/活动)、描述、地址、地理坐标
- 关联城市、图片、标签

### 收藏 (Favorite)
- 用户ID(可为空表示游客)、访客ID、项目ID、项目类型
- 关联用户

## 安装与运行

1. 安装依赖：
```
pip install -r requirements.txt
```

2. 初始化数据库：
```
python init_db.py
```

3. 运行应用：
```
uvicorn app.main:app --reload
```

4. 访问API文档：http://localhost:8000/docs

## 依赖库

- fastapi
- uvicorn
- sqlalchemy
- passlib[哈希]
- bcrypt
- python-jose[cryptography]
- pydantic[email]

## API文档

启动应用后，可通过以下URL访问自动生成的API文档：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

