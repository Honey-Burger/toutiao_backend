from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config.db_config import get_database
from models.users import User
from schemas.users import UserRequest, UserAuthResponse, UserInfoResponse, UserUpdateRequest
from crud import users
from utils.auth import get_current_user
from utils.response import success_response

router = APIRouter(prefix = "/api/user", tags =["users"])

@router.post("/register")
async def register(user_data: UserRequest,db: AsyncSession = Depends(get_database)):
    # 注册逻辑：验证数据库是否存在，创建用户，生成Token，响应结果
    exciting_user =  await users.get_user_by_username(db, user_data.username)
    if exciting_user:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户已存在")
    user = await users.create_user(db, user_data)
    token =await users.create_token(db,user.id)
#     return {
#   "code": 200,
#   "message": "注册成功",
#   "data": {
#     "token": token,
#     "userInfo": {
#       "id": user.id,
#       "username":user.username,
#       "bio": user.bio,
#       "avatar": user.avatar
#     }
#   }
# }
    response_data = UserAuthResponse(
        token = token,
        userInfo = UserInfoResponse.model_validate(user)
        #直接接收ORM对象，转换成前端能看懂的 JSON 模型
        #这里useInfo只会存UserInfoResponse类里定义的字段，未定义的不会显示，会直接被过滤掉
    )
    return success_response(message = "注册成功", data = response_data)

@router.post("/login")
async def login(user_data: UserRequest,db: AsyncSession = Depends(get_database)):
    # 登录逻辑：验证数据库是否存在用户，验证密码，生成Token，响应结果
    user = await users.authenticate_user(db, user_data.username, user_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")
    token = await users.create_token(db,user.id)
    response_data = UserAuthResponse(
        token = token,
        userInfo = UserInfoResponse.model_validate(user)
    )

    return success_response(message = "登录成功", data = response_data)

@router.get("/info")#查Token用户 → 封装CRUD → 功能整合成一个工具函数 → 路由导入使用：依赖注入
async def get_user_info(user :User = Depends(get_current_user)):
    return success_response(
        message = "获取用户信息成功",
        data = UserInfoResponse.model_validate( user))

#修改用户信息：验证Token → 验证用户是否存在 → 修改用户信息（用户输入数据 put提交 → 请求体参数 → 定义Pydantic模型类）→ 响应结果
#参数： 用户输入的 + 验证Token的 + db（调用更新的方法）
@router.put("/info")
async def update_user_info(user_data: UserUpdateRequest,
                           user: User = Depends(get_current_user),
                           db: AsyncSession = Depends(get_database)
                           ):
    # 修改用户信息逻辑：验证数据库是否存在用户，修改用户信息，响应结果
    return success_response(message = "修改用户信息成功")
