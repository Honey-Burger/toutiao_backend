import json
from typing import Any

import redis.asyncio as redis
from pymysql import protocol

REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
#创建 Redis 的连接对象
redis_client = redis.Redis(
    host=REDIS_HOST,#Redis 服务器的主机名或 IP 地址
    port=REDIS_PORT,#Redis 服务器的端口号
    db=REDIS_DB,#Redis 数据库的索引
    decode_responses=True, #告诉Redis返回的字符串结果，而不是字节结果
    protocol = 2
)

#设置 和 读取（字符串 和 列表或字典这两个方法） "[{}]"

#读取：字符串
async def get_cache(key: str):
    try:#有可能获取不到
        return await redis_client.get(key)
    except Exception as e:
        print(f"获取缓存失败:{e}")
        return None

#读取：列表或字典
async def get_json_cache(key: str):
    try:
        data = await redis_client.get(key)
        if data:
            return json.loads(data)#把json字符串转Python字典
        return None
    except Exception as e:
        print(f"获取缓存失败:{e}")
        return None

#设置缓存 setex(key, expire, value)
async def set_cache(key: str, value: Any, expire: int = 3600):
    try:
        if isinstance(value,(dict, list)):#如果是字典或列表
            #转字符串再存储
            value = json.dumps(value, ensure_ascii=False)#不转码，存储中文
        print(f"🔴 设置缓存: key={key}, expire={expire}s, value类型={type(value)}")
        await redis_client.setex(key, expire, value)
        print(f"✅ 缓存设置成功")
        return True
    except Exception as e:
        print(f"❌ 设置缓存失败:{e}")
        return False
