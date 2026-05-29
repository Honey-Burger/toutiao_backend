from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from schemas.base import NewsItemBase


class HistoryAddRequest(BaseModel):
    """
    添加浏览记录的请求模型
    用于接收前端传来的新闻ID
    """
    news_id: int = Field(..., alias="newsId")  # 新闻ID，必填字段，使用驼峰命名别名


class HistoryNewsItemResponse(NewsItemBase):
    """
    浏览历史项响应模型
    继承自 NewsItemBase，包含新闻基本信息 + 浏览记录特有字段
    """
    history_id: int = Field(alias="historyId")  # 浏览记录ID，使用驼峰命名别名
    view_time: datetime = Field(alias="viewTime")  # 浏览时间，使用驼峰命名别名

    model_config = ConfigDict(
        populate_by_name=True,   # 允许同时使用字段名和别名进行序列化/反序列化
        from_attributes=True,    # 允许从 ORM 对象属性获取值（支持 SQLAlchemy 模型）
    )


class HistoryListResponse(BaseModel):
    """
    浏览历史列表响应模型
    用于返回分页的浏览历史数据
    """
    list: list[HistoryNewsItemResponse]  # 浏览历史记录列表
    total: int  # 总记录数
    has_more: bool = Field(alias="hasMore")  # 是否还有更多数据（分页标识）

    model_config = ConfigDict(
        populate_by_name=True,   # 允许同时使用字段名和别名进行序列化/反序列化
        from_attributes=True,    # 允许从 ORM 对象属性获取值（支持 SQLAlchemy 模型）
    )
