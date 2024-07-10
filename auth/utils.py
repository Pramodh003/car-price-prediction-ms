from passlib.context import CryptContext
from .service.redis_service import check_user_in_redis, write_to_redis, read_from_redis
from .oauth2 import get_current_user
from fastapi import Request
pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")


def hash(password: str):
    return pwd_context.hash(password)





def verify(token, plain_password,db):
    # if not check_user_in_redis(id):
        cookie_authorization: str = Request.cookies.get("Authorization")
        print(cookie_authorization)
        # return None
    # data = read_from_redis(username)
    # print(data)
    # if pwd_context.verify(plain_password, data["hashed_password"]):
        # if data["status"] == "PASSIVE":
        #     data["status"] = "ACTIVE"
        #     write_to_redis(username, data)
        #     data = read_from_redis(username)
        # return data["id"]
    # return False

    