from pydantic import BaseModel
#类型校验代码
class UserRequest(BaseModel):
    username: str
    password: str