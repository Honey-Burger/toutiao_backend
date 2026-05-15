from passlib.context import CryptContext
# 创建密码上下文
pwd_context =CryptContext(schemes=["bcrypt"], deprecated="auto")
#全局密码加密工具实例
#给用户密码密码加米
def get_hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
    # 验证密码,返回值为布尔值