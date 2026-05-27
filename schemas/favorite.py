from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

from schemas.base import NewsItemBase


class FavoriteCheckResponse(BaseModel):
    is_favorite: bool = Field(...,alias = "isFavorite")

class FavoriteAddRequest(BaseModel):
    news_id: int = Field(..., alias="newsId")

#规划两个类： 一个是新闻模型类， 一个是收藏列表响应模型类，增强复用性
class FavoriteNewsItemResponse(NewsItemBase):
    favorite_id: int = Field(alias="favoriteId")
    favorite_time: datetime = Field(alias="favoriteTime")
    model_config = ConfigDict(
        populate_by_name = True, #alas / 字段名兼容
        from_attributes = True,# 允许从 ORM 对象获取值
    )
#收藏列表响应模型类
class FavoriteListResponse(BaseModel):
    list: list[FavoriteNewsItemResponse]
    total: int
    has_more: bool = Field(alias = "hasMore")
    model_config = ConfigDict(
        populate_by_name = True, #alas / 字段名兼容
        from_attributes = True,# 允许从 ORM 对象获取值
    )

