from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from models.favorite import Favorite


async def is_news_favorite(db: AsyncSession,
                           user_id: int,
                           news_id: int
):
    query = select(Favorite).where(Favorite.user_id == user_id,Favorite.news_id == news_id)
    result = await db.execute(query)
    #是否有收藏记录
    return result.scalar_one_or_none() is not None#判断语句：有收藏记录返回True，无收藏记录返回False

async def add_news_favorite(db: AsyncSession,
                           user_id: int,
                           news_id: int
):
    favorite = Favorite(user_id=user_id, news_id=news_id)#创建ORM实例
    db.add(favorite)
    """
    Favorite 实例是全新的、未被数据库管理的对象，
    db.add() 的作用就是把它 “注册” 到当前会话，让 SQLAlchemy 知道要把它插入到数据库。
    """
    await db.commit()
    await db.refresh(favorite)
    return favorite

async def remove_news_favorite(db: AsyncSession,
                           user_id: int,
                           news_id: int
):
    favorite =Favorite(user_id=user_id, news_id=news_id)
    if favorite:#如果收藏记录存在，则删除
        stmt = delete(Favorite).where(Favorite.user_id == user_id,Favorite.news_id == news_id)
        result = await db.execute(stmt)
        await db.commit()
        return result.rowcount > 0#删除成功返回True，否则返回False
