from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_config import get_database
from crud import news

#创建APIrouter实例
# prefix 路由前缀 （主要根据API接口文档书写）
# tags 分组 标签
router = APIRouter(prefix = "/api/news", tags =["news"] )

@router.get("/categories")
async def get_categories(
        skip: int = 0,
        limit: int = 10,
        db: AsyncSession = Depends(get_database)
):
    #先获取数据库里面新闻分类数据 →先定义模型类 → 封装查询数据方法
    categories = await news.get_categories(db, skip, limit)
    return {
        "code": 200,
        "message": "获取新闻分类成功",
        "data": categories
    }

# 新闻列表接口：GET 请求 /api/news/list
@router.get("/list")
async def get_news_list(
        # 前端传分类ID，别名categoryId（驼峰命名），必填
        category_id: int = Query(..., alias="categoryId"),
        # 页码，默认第1页
        page: int = 1,
        # 每页条数，默认10，最大不超过100，别名pageSize
        page_size: int = Query(10, alias="pageSize", le=100),
        # 依赖注入：获取数据库异步会话
        db: AsyncSession = Depends(get_database)
):
    # 分页计算：offset = 第几条开始（跳过前面的数据）
    offset = (page - 1) * page_size

    # 调用DAO层方法：查询当前页的新闻列表
    news_list = await news.get_news_list(db, category_id, offset, page_size)

    # 调用DAO层方法：统计该分类下新闻总条数
    total = await news.get_news_count(db, category_id)
    has_more = (offset + len(news_list)) < total

    # 统一返回格式：code、message、data（列表+总数）
    return {
        "code": 200,
        "message": "获取新闻列表成功",
        "data": {
            "list": news_list,    # 当前页新闻数据
            "total": total,       # 总条数（用于前端分页）
            "hasMore": has_more  # 是否有下一页
        }
    }

@router.get("/detail")
async def get_news_detail(
    id: int = Query(..., alias="id"),
    db: AsyncSession = Depends(get_database)
):#获取新闻详情+浏览量+1+相关新闻
    news_detail = await news.get_news_detail(db, id)
    if not news_detail:#检查新闻是否存在，如果不存在，直接返回 404 给前端，终止后续流程
        raise HTTPException(status_code=404, detail="新闻不存在")

    views_res = await news.increase_news_views(db, news_detail.id)
    if not views_res:#检查更新操作是否真的命中了数据。
        raise HTTPException(status_code=404, detail="新闻不存在")
    related_news = await news.get_news_list(db, news_detail.id, news_detail.category_id, limit = 5)
    return {
            "code": 200,
            "message": "success",
            "data": {
                "id": news_detail.id,
                "title": news_detail.title,
                "content": news_detail.content,
                "image": news_detail.image,
                "author": news_detail.author,
                "publishTime": news_detail.publish_time,
                "categoryId": news_detail.category_id,
                "views": news_detail.views,
                "relatedNews": related_news
            }
    }
