from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config.db_config import get_database
from crud import history
from models.users import User
from schemas.history import HistoryAddRequest, HistoryListResponse
from utils.auth import get_current_user
from utils.response import success_response

router = APIRouter(prefix="/api/history", tags=["history"])


@router.post("/add")
async def add_history(
        data: HistoryAddRequest,
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_database)
):
    result = await history.add_news_history(db, user.id, data.news_id)
    return success_response(message="添加浏览记录成功", data=result)


@router.get("/list")
async def get_history_list(
        page: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1, le=100, alias="pageSize"),
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_database)
):
    total, rows = await history.get_history_list(db, user.id, page, page_size)
    history_list = [
        {
            "id": news.id,
            "title": news.title,
            "description": news.description,
            "image": news.image,
            "author": news.author,
            "categoryId": news.category_id,
            "views": news.views,
            "publishedTime": news.publish_time,
            "viewTime": view_time,
            "historyId": history_id
        } for news, view_time, history_id in rows
    ]
    has_more = total > page * page_size
    data = HistoryListResponse(
        total=total,
        hasMore=has_more,
        list=history_list
    )
    return success_response(message="获取浏览历史成功", data=data)






@router.delete("/remove")
async def remove_history(
        news_id: int = Query(..., alias="newsId"),
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_database)
):
    result = await history.remove_history(db, user.id, news_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="浏览记录不存在")
    return success_response(message="删除浏览记录成功", data=result)


@router.delete("/clear")
async def clear_history(
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_database)
):
    count = await history.remove_all_history(db, user.id)
    return success_response(message=f"清空了{count}条浏览记录")
