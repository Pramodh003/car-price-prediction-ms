import json
from ..config.redis_db import redis_client

def write_to_redis(key, value):
    redis_client.set(key, json.dumps(value))
    
def read_from_redis(key):
    return json.loads(redis_client.get(key))

def check_user_in_redis(username):
    return redis_client.exists(username)