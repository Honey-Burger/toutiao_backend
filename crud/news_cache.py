from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from cache.news_cache import get_cached_categories, set_cached_categories, get_cache_news_list, set_cached_news_list
from models.news import Category, News
from schemas.base import NewsItemBase


# 1. 获取所有新闻分类（带分页：跳过多少条、取多少条）
async def get_categories(
    db: AsyncSession,  # 数据库异步会话
    skip: int = 0,     # 分页：跳过前N条（默认不跳过）
    limit: int = 10    # 分页：最多取N条（默认10条）
):
    #先尝试从缓存中获取数据
    cached_categories = await get_cached_categories()
    if cached_categories:
        print(f"✅ 命中缓存: {cached_categories}")
        return cached_categories

    print("❌ 缓存未命中，查询数据库...")

    # 构建SQL：查询Category表，跳过skip条，限制limit条
    stmt = select(Category).offset(skip).limit(limit)
    # 执行SQL语句
    result = await db.execute(stmt)
    categories = result.scalars().all()

    print(f"数据库查询结果: {categories}, 数量: {len(categories)}")

    #写入缓存
    if categories:
        categories_encoded = jsonable_encoder(categories)
        print(f"准备写入缓存: {categories_encoded}")
        success = await set_cached_categories(categories_encoded)
        print(f"缓存写入结果: {'成功' if success else '失败'}")
    else:
        print("⚠️ 数据库无数据，不写入缓存")

    #返回数据
    return categories
'''
# 1. 获取所有新闻分类（带分页：跳过多少条、取多少条）
async def get_categories(
    db: AsyncSession,  # 数据库异步会话
    skip: int = 0,     # 分页：跳过前N条（默认不跳过）
    limit: int = 10    # 分页：最多取N条（默认10条）
):
    #先尝试从缓存中获取数据
    cached_categories = await get_cached_categories()
    if cached_categories:
        return cached_categories

    # 构建SQL：查询Category表，跳过skip条，限制limit条
    stmt = select(Category).offset(skip).limit(limit)
    # 执行SQL语句
    result = await db.execute(stmt)
    categories =  result.scalars().all()

    #写入缓存
    if categories:
        categories = jsonable_encoder( categories)
        await set_cached_categories( categories)

    #返回数据
    return categories
'''

# 2. 根据分类ID获取新闻列表（带分页）
async def get_news_list(
    db: AsyncSession,      # 数据库异步会话
    category_id: int,      # 新闻分类ID（要查哪个分类下的新闻）
    skip: int = 0,         # 分页：跳过N条
    limit: int = 10       # 分页：取N条
):
    # 先尝试从缓存中获取数据
    #await get_cache_new_list(分类_id,页码,每页数量)
    # 构建SQL：查询News表，筛选分类ID=指定值，分页
    page = skip//limit + 1 #页码 = 跳过条数 // 每页数量 +1
    cached_list = await get_cache_news_list(category_id, page, limit)#
    if cached_list:
        return cached_list # 返回字典列表，FastAPI 也能处理

    stmt = select(News).where(News.category_id == category_id).offset(skip).limit(limit)
    # 执行SQL
    result = await db.execute(stmt)
    # 返回新闻列表
    news_list = result.scalars().all()

    # 写入缓存
    if news_list:
        #先把 ORM 数据 转换成 字典 才能写入缓存
        #ORM 转成 Pydantic，再转成 字典
        #by_alias=False 不使用别名，因为Redis数据是给后端用的
        news_data = [NewsItemBase.model_validate(item).model_dump(mode="json", by_alias=False) for item in news_list]
        await set_cached_news_list(category_id, page, limit, news_data)

    return news_list


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