# from app.database import engine
# from app import models

# # 创建所有表
# models.Base.metadata.create_all(bind=engine) 


from app.database import SessionLocal
from app import models
from app.utils.security import get_password_hash
from sqlalchemy.exc import IntegrityError

# 创建数据库会话
db = SessionLocal()

# 检查测试用户是否已存在
existing_user = db.query(models.User).filter(models.User.username == "测试用户").first()
if not existing_user:
    # 添加测试用户
    test_user = models.User(
        username="测试用户",
        email="test@example.com",
        hashed_password=get_password_hash("password123")
    )
    db.add(test_user)

# 检查城市是否已存在
existing_city = db.query(models.City).filter(models.City.name == "北京").first()
if not existing_city:
    # 添加示例城市
    example_city = models.City(
        name="北京",
        province="北京市",
        region="华北",
        description="中国首都，历史文化名城",
        current_temperature=25.5,
        best_season="秋季",
        latitude=39.9042,
        longitude=116.4074
    )
    db.add(example_city)

try:
    # 提交更改
    db.commit()
    print("数据库初始化成功！")
except IntegrityError as e:
    db.rollback()
    print(f"数据库约束错误: {e}")
finally:
    db.close()