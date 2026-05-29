from sqlalchemy import select, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from models.history import History
from models.news import News


async def add_news_history(db: AsyncSession,
                           user_id: int,
                           news_id: int
):
    """添加浏览记录"""
    history_record = History(user_id=user_id, news_id=news_id)
    db.add(history_record)
    await db.commit()
    await db.refresh(history_record)
    return history_record


async def get_history_list(
        db: AsyncSession,
        user_id: int,
        page: int = 1,
        page_size: int = 10
):
    """获取浏览历史列表：获取某个用户的浏览历史 + 分页功能"""
    # 总量统计
    count_query = select(func.count()).where(History.user_id == user_id)
    count_result = await db.execute(count_query)
    total = count_result.scalar_one()

    offset = (page - 1) * page_size

    # 获取浏览历史列表 - 从 History 表开始查询，JOIN News 表获取新闻详情
    query = (select(News,
                    History.view_time.label("view_time"),
                    History.id.label("history_id"))
             .select_from(History)
             .join(News, History.news_id == News.id)
             .where(History.user_id == user_id)
             .order_by(History.view_time.desc())
             .offset(offset)
             .limit(page_size)
             )
    result = await db.execute(query)
    rows = result.all()

    return total, rows


async def remove_history(db: AsyncSession,
                         user_id: int,
                         news_id: int
):
    """删除单条浏览记录"""
    stmt = delete(History).where(
        History.user_id == user_id,
        History.news_id == news_id
    )
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0


async def remove_all_history(
        db: AsyncSession,
        user_id: int
):
    """清空浏览历史"""
    stmt = delete(History).where(History.user_id == user_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount or 0
