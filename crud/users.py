from datetime import timedelta,datetime
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.users import User, UserToken
from schemas.users import UserRequest
from utils import security

#根据用户名查询数据库,是否存在数据
async def get_user_by_username(db: AsyncSession, username: str):
    query = select(User).where(User.username == username)
    result = await db.execute(query)
    return result.scalar_one_or_none()

#创建用户
async def create_user(db: AsyncSession, user_data: UserRequest):
    #先进行密码加密，切不可直接把密码保存在数据库中
    hashed_password = security.get_hash_password(user_data.password)#调用自己写的密码加密方法
    user = User(username=user_data.username, password=hashed_password)
    db.add(user)
    await db.commit()
    await db.refresh(user)#refresh 的作用：获取数据库自动生成的字段（特别是 id）！
    return user

#生成 Token
async def create_token(db: AsyncSession, user_id: int):
    # 生成 Token + 设置过期时间 + →查询数据库当前用户是否有 Token → 有：更新；没有：添加
    token = str(uuid.uuid4())#生成随机字符串
    # timedelta(day=7, hours=2, minutes=30, second=10),这是一个时间间隔对象，表示7天2小时30分10秒
    expires_at = datetime.now() + timedelta(days=7)#计算出 Token 的过期时间 = 当前时间 + 7 天
    query = select(UserToken).where(UserToken.id == user_id)
    result = await db.execute(query)
    user_token = result.scalar_one_or_none()
    if user_token:#如果存在，更新
        user_token.token = token
        user_token.expires_at = expires_at
    else:#不存在，添加
        user_token = UserToken(user_id=user_id, token=token, expires_at=expires_at)
        db.add(user_token)
        await db.commit()
    return token#返回最新生成的 Token