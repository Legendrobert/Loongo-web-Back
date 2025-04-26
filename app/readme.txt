##1、环境配置
# 复制环境变量示例文件
cp .env.example .env  # Linux/Mac
# 或
copy .env.example .env  # Windows

##2、使用
# PowerShell临时设置
$env:SECRET_KEY = "your_secure_random_key"
$env:DATABASE_URL = "sqlite:///./app.db"

# 或永久设置(管理员权限)
[Environment]::SetEnvironmentVariable("SECRET_KEY", "your_secure_random_key", "Machine")

##3、启动
# 开发模式（自动重载）
uvicorn main:app --reload

# 生产模式
uvicorn main:app --host 0.0.0.0 --port 8000

应用启动后可访问:
API接口: http://127.0.0.1:8000
API文档: http://127.0.0.1:8000/docs
健康检查: http://127.0.0.1:8000/health


登录与游客态
系统支持两种用户状态:
登录用户：通过JWT令牌验证，可使用所有功能
使用/auth/register注册新用户
使用/auth/token获取登录令牌
游客用户：通过Cookie中的visitor_id标识
可浏览内容并收藏
收藏数据临时存储
登录后游客数据自动合并到用户账户