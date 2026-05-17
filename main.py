from fastapi import FastAPI
from routers import news,users
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from utils.exception_handlers import register_exception_handlers

app = FastAPI()
# 注册异常处理
register_exception_handlers(app)

app.add_middleware(#解决跨域问题
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"}

#挂载路由/注册路由
app.include_router(news.router)
app.include_router(users.router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)