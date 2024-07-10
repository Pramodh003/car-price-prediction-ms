from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_hostname: str
    database_username: str
    database_password: str
    database_port: int
    database_name: str
    secret_key: str
    algorithm: str
    access_token_expire_minute: int
    redis_host: str
    redis_port: str
    redis_password: str
    
    class Config:
        env_file = ".env"
        
settings = Settings()
    