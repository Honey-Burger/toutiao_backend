import uuid
from datetime import timedelta, datetime

from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from models.users import User, UserToken
from schemas.users import UserRequest, UserUpdateRequest
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

async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_user_by_username(db, username)#获取用户(有可能没有)
    if not user:#用户不存在,返回 None
        return None
    if not security.verify_password(password, user.password):#密码验证失败，返回 None
        return None
    return user#密码验证成功，返回用户对象

#根据 Token 查询用户 ： 验证 Token → 验证用户
async def get_user_by_token(db: AsyncSession, token: str):
    query = select(UserToken).where(UserToken.token == token)
    result = await db.execute(query)
    db_token = result.scalar_one_or_none()
    if not db_token or db_token.expires_at < datetime.now():
        return None

    query = select(User).where(User.id == db_token.user_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()
    """
    这里为什么还要使用scalar_one_or_none()：
    如果数据库出现脏数据（比如 user_id 重复），
    scalar_one() 会直接炸，
    而 scalar_one_or_none() 至少能让你拿到 None，再在调用层处理。
    """

#更新用户信息
async def update_user(db: AsyncSession,username: str,
                      user_data: UserUpdateRequest,
                      ):
    # update(User).where(User.name == username).values(字段 = 值)
    # user_data 是一个Pydantic类型对象，必须进行解包变成字典才能变成字段=值的形式使用
    #没有设置值的不更新
    query = update(User).where(User.username == username).values(**user_data.model_dump(
        exclude_unset= True,
        exclude_none= True  ))#修改操作
    result = await db.execute(query)
    await db.commit()
    #检查更新
    if result.rowcount == 0:#如果用户不存在，更新失败，抛出异常
        raise HTTPException(status_code=404, detail="用户不存在")
    #获取更新后的用户信息
    updated_user = await get_user_by_username(db, username)
    return updated_user