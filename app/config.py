import os
from dotenv import load_dotenv

load_dotenv() 

class Settings:
    PROJECT_NAME: str = "NOESIS EEG API"
    VERSION: str = "1.0.0"

    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    DATABASE_USER: str = os.getenv("DATABASE_USER")
    DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME")
    DATABASE_PORT: str = os.getenv("DATABASE_PORT")



settings = Settings()
