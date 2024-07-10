from passlib.context import CryptContext
from .service.redis_service import check_user_in_redis, write_to_redis, read_from_redis
from .oauth2 import get_current_user

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")


def hash(password: str):
    return pwd_context.hash(password)


def verify(token, plain_password, db):
    if not check_user_in_redis(token):
        return None
    data = read_from_redis(token)
    print(data['id'])
    if pwd_context.verify(plain_password, data["hashed_password"]):
        return data["id"]
    return False

    