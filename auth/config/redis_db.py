import redis
 
from .config import settings

redis_client = redis.Redis.from_url(settings.redis_url)
# redis = get_redis_connection(
#     host = settings.redis_host,
#     port=settings.redis_port,
#     password=settings.redis_password,
#     decode_responses=True
# )

print(redis_client)