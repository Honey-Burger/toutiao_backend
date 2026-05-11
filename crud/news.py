

from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession
from models.news import Category, News


# 1. 获取所有新闻分类（带分页：跳过多少条、取多少条）
async def get_categories(
    db: AsyncSession,  # 数据库异步会话
    skip: int = 0,     # 分页：跳过前N条（默认不跳过）
    limit: int = 10    # 分页：最多取N条（默认10条）
):
    # 构建SQL：查询Category表，跳过skip条，限制limit条
    stmt = select(Category).offset(skip).limit(limit)
    # 执行SQL语句
    result = await db.execute(stmt)
    # 获取所有结果并返回（返回列表）
    return result.scalars().all()


# 2. 根据分类ID获取新闻列表（带分页）
async def get_news_list(
    db: AsyncSession,      # 数据库异步会话
    category_id: int,      # 新闻分类ID（要查哪个分类下的新闻）
    skip: int = 0,         # 分页：跳过N条
    limit: int = 10       # 分页：取N条
):
    # 构建SQL：查询News表，筛选分类ID=指定值，分页
    stmt = select(News).where(News.category_id == category_id).offset(skip).limit(limit)
    # 执行SQL
    result = await db.execute(stmt)
    # 返回新闻列表
    return result.scalars().all()


# 3. 根据分类ID统计该分类下一共有多少条新闻（给分页用）
async def get_news_count(
    db: AsyncSession,      # 数据库异步会话
    category_id: int       # 分类ID
):
    # 构建SQL：统计News表中，该分类下的新闻总数量 count(id)
    stmt = select(func.count(News.id)).where(News.category_id == category_id)
    # 执行SQL
    result = await db.execute(stmt)
    # 返回唯一的统计结果（总条数）
    return result.scalar_one()

# 4. 根据新闻ID获取新闻详情
async def get_news_detail(
    db: AsyncSession,
    news_id: int
):
    # 构建SQL：查询News表，筛选ID=指定值
    stmt = select(News).where(News.id == news_id)
    # 执行SQL
    result = await db.execute(stmt)
    # 获取结果并返回
    return result.scalar_one_or_none()

# 5. 根据新闻ID更新新闻浏览量
async def increase_news_views(
        db: AsyncSession,
        news_id: int
):
    stmt = update(News).where(News.id == news_id).values(views = News.views + 1)
    result = await db.execute(stmt)
    await db.commit()
# 我在异步引擎那里不是写了提交数据库吗？为啥这里还要写？
# db_config 里的 commit：管整个请求的事务，最后才执行。
# 函数里的 commit：管当前这条更新操作，让修改立刻生效。
# 你现在要的是「浏览量 +1 后马上能看到新值」，所以必须在 increase_news_views 里写 await db.commit()。

#更新 → 检查数据库是否是否真的命中了数据 → 命中了返回True
    return result.rowcount > 0 #如果本次更新操作影响了至少 1 行数据 → 返回 True，否则返回 False

async def get_related_news(
    db: AsyncSession,
    news_id: int,
    category_id: int,
    limit : int = 10
):
    stmt = select(News).where(
        News.category_id == category_id,
        News.id != news_id
    ).order_by(#排序
        News.views.desc(),#默认是升序，降序是desc()
        News.publish_time.desc()
    ).limit(limit)#限制5个
    result = await db.execute(stmt)
    related_news = result.scalars().all()
    # 列表推导式 推导出新闻的核心数据，然后再 return
    return [
        {
            "id": news_detail.id,
            "title": news_detail.title,
            "content": news_detail.content,
            "image": news_detail.image,
            "author": news_detail.author,
            "publishTime": news_detail.publish_time,
            "categoryId": news_detail.category_id,
            "views": news_detail.views
        }
        for news_detail in related_news
    ]