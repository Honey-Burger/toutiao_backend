from sqlalchemy import select, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from models.favorite import Favorite
from models.news import News


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

#获取收藏列表：获取某个用户的收藏列表 + 分页功能
async def get_favorite_list(
        db: AsyncSession,
        user_id: int,
        page: int = 1,
        page_size: int = 10
):
    # 总量 + 收藏的新闻列表
    count_query = select(func.count()).where(Favorite.user_id == user_id)
    #这里的 func.count() 是聚合函数，数据库会计算后返回一行一列的结果
    count_result = await db.execute(count_query)#执行 SQL
    total = count_result.scalar_one()
    offset = (page - 1) * page_size
    #获取收藏列表 - 联表查询 join() + 收藏时间排序 + 分页
    #select(查询主体模型类，字段别名).join(联合查询的模型类，联合查询的条件).where(条件).order_by().offset().limit()
    #别名： Favorite.created_at.label("favorite_time")
    query = (select(News, Favorite.created_at.label("favorite_time"), Favorite.id.label("favorite_id"))
                   .join(Favorite, Favorite.news_id == News.id).
                   where(Favorite.user_id == user_id).order_by(Favorite.created_at.desc())#按照收藏的时间降序
                   .offset(offset).limit(page_size)
             )
    result = await db.execute(query)
    row = result.all()
    return total, row
'''row = [
    (News对象1, datetime1, favorite_id1),
    (News对象2, datetime2, favorite_id2),
    (News对象3, datetime3, favorite_id3),
    ...
]
'''

