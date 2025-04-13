from passlib.context import CryptContext

# 使用sha256_crypt替代bcrypt
pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

# 验证密码
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# 生成密码哈希
def get_password_hash(password):
    return pwd_context.hash(password) 