from datetime import datetime
from sqlalchemy import func
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql.sqltypes import String, Float, DateTime
ASYNC_DATABASE_URL = "mysql+aiomysql://root:123456@localhost:3306/news_app?charset=utf8"
#这是数据库连接字符串，告诉程序连哪个数据库
#mysql+aiomysql：使用 MySQL 数据库 + 异步驱动 aiomysql
#root：数据库用户名
#123456：数据库密码
#localhost：数据库在本机
#3306：MySQL 默认端口
#FastAPI_first：要连接的数据库名
#charset=utf8：字符编码，支持中文
#创建异步引擎
async_engine = create_async_engine(#异步引擎的配置
    ASYNC_DATABASE_URL,#数据库连接地址()
    echo=True,#可选，输出 SQL 日志
    pool_size=10,#设置连接池活跃的连接数
    max_overflow=20)#允许额外的连接数，也就是说对多能连接30个

class Base(DeclarativeBase):#创建基类
    create_time : Mapped[datetime] = mapped_column(
        DateTime,
        nsert_default=func.now(),
        default=func.now, comment = "创建时间")
    update_time : Mapped[datetime] = mapped_column(
        DateTime,
        insert_default=func.now(),
        default=func.now,
        onupdate=func.now(),
        comment="修改时间")
#创建异步会话工厂
AsyncSessionLocal = async_sessionmaker(
    bind = async_engine, # 绑定数据库引擎
    class_ = AsyncSession, #指定异步会话类
    expire_on_commit= False#提交后会话不会过期，不会重新查询数据库
)

#依赖项函数，用于获取数据库会话
async def get_database():
    async with AsyncSessionLocal() as session:
        try:
            yield session #返回数据库会话给路由处理函数
            await session.commit()#提交事务
        except Exception:
            await session.rollback()# 如果有异常，回滚
            raise
        finally:
            await session.close()#关闭会话

