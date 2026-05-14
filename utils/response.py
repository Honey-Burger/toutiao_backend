from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
def success_response(message: str = "success", data = None):
    content = {
        "code": 200,
        "message": message,
        "data": data
    }
    #data的数据格式多变，重点是data的数据结构怎么定义。通过schemas/users.py中的UserAuthResponse类定义

    #目标：把任何的FastAPI、Pydantic、ORM 对象都要正常响应 → code、message、data
    return JSONResponse(content=jsonable_encoder( content))
    #jsonable_encode 就是把「Python 不能转成 JSON 的东西」变成「能转成 JSON 的东西」
    #JSONResponse = 告诉前端：我给你返回的是 JSON 格式！