from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")
from 
def verify(username, plain_password, db):
    if not check_user_in_redis(username):
        return None
    