from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "mysql+pymysql://user:password@localhost/blog_db"
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    CACHE_EXPIRE_SECONDS: int = 300  # 5 minutes

    class Config:
        env_file = ".env"

settings = Settings()