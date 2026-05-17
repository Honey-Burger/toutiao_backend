#整合 根据 Token 查询用户，返回用户
from fastapi import Header, Depends,HTTPException
from starlette import status
from config.db_config import get_database
from crud import users

async def get_current_user(
        authorization: str = Header(..., alias="Authorization"),
        db = Depends(get_database)
):
    #前端传过来：Bearer eyJxxxxxxxxxxx.token.string, 这里只取token
    token = authorization.replace("Bearer", "")
    """
    方法二：token = authorization.split(" ")[1],也就是把列表分割，取后面那个。
    """
    user = await users.get_user_by_token(db, token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="无效的令牌或已经过期的的令牌")
    return user