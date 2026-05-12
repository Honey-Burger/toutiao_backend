from passlib.context import CryptContext
# 创建密码上下文
pwd_context =CryptContext(schemes=["bcrypt"], deprecated="auto")
#全局密码加密工具实例
#密码加米
def get_hash_password(password: str):
    return pwd_context.hash(password)