from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


#类型校验代码
class UserRequest(BaseModel):
    username: str
    password: str

#user_ info 对应的类：基础类 + Info 类 （id、用户名）
class UserInfoBase(BaseModel):
    nickname: Optional[str] = Field(None, max_length=50, description="用户昵称")
    avatar: Optional[str] = Field(None, max_length=255, description="用户头像地址")
    gender: Optional[str] = Field(None, max_length=10, description="用户性别")
    bio: Optional[str] = Field(None, max_length=500, description="个人简介")

class UserInfoResponse(UserInfoBase):
    id: int
    username: str
    # 模型类配置
    model_config = ConfigDict(
        from_attributes=True,  # 允许从 ORM 对象获取值
    )
#data 数据类型
class UserAuthResponse(BaseModel):
    token: str
    user_info: UserInfoResponse = Field(..., alias = "userInfo")

    #模型类配置
    model_config = ConfigDict(
        populate_by_name = True, #alas / 字段名兼容
        #你可以写 UserAuthResponse(user_info=xxx) ✅
        #也可以写 UserAuthResponse(userInfo=xxx) ✅
        from_attributes = True,# 允许从 ORM 对象获取值
    )