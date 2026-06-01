import redis.asyncio as redis

REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
#创建 Redis 的连接对象
redis_client = redis.Redis(
    host=REDIS_HOST,#Redis 服务器的主机名或 IP 地址
    port=REDIS_PORT,#Redis 服务器的端口号
    db=REDIS_DB,#Redis 数据库的索引

    decode_responses=True#告诉 Redis 返回的字符串结果，而不是字节结果
)