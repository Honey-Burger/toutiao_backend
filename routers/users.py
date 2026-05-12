from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config.db_config import get_database
from schemas.users import UserRequest
from crud import users
router = APIRouter(prefix = "/api/user", tags =["users"])

@router.post("/register")
async def register(user_data: UserRequest,db: AsyncSession = Depends(get_database)):
    # 注册逻辑：验证数据库是否存在，创建用户，生成Token，响应结果
    exciting_user =  await users.get_user_by_username(db, user_data.username)
    if exciting_user:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户已存在")
    user = await users.create_user(db, user_data)
    return {
  "code": 200,
  "message": "注册成功",
  "data": {
    "token": "用户访问令牌",
    "userInfo": {
      "id": user.id,
      "username":user.username,
      "bio": user.bio,
      "avatar": user.avatar
    }
  }
}