from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

class NewsItemBase(BaseModel):
    """
    新闻项基础数据模型（用于API响应/请求的数据验证和序列化）

    作用：
    1. 定义新闻数据的结构规范
    2. 自动验证数据类型（比如 id 必须是 int，title 必须是 str）
    3. 支持字段别名（Python用下划线命名，前端用驼峰命名）
    4. 将数据库ORM对象转换为JSON格式返回给前端
    """
    id: int                              # 新闻ID
    title: str                           # 新闻标题
    description: Optional[str] = None    # 新闻简介（可选字段，可能为空）
    image: Optional[str] = None          # 封面图片URL（可选字段，可能为空）
    author: Optional[str] = None         # 作者（可选字段，可能为空）
    category_id: int = Field(alias="categoryId")           # 分类ID（后端用category_id，前端传categoryId）
    views: int                           # 浏览量
    publish_time: Optional[datetime] = Field(None, alias="publishedTime")  # 发布时间（后端用publish_time，前端传publishedTime）

    model_config = ConfigDict(
        from_attributes=True,      # 允许从ORM对象（如News模型）创建实例，支持数据库对象转Pydantic模型
        populate_by_name=True      # 同时支持使用字段名（category_id）和别名（categoryId）进行赋值
    )
