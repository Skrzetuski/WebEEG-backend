from sqlalchemy import create_engine
from sqlalchemy import URL
from sqlalchemy.orm import sessionmaker
from config import settings

url_db = URL.create(
    "postgresql",
    username=settings.DATABASE_USER,
    password=settings.DATABASE_PASSWORD,  
    host=settings.DATABASE_URL,
    database=settings.DATABASE_NAME,
    port= settings.DATABASE_PORT,
)

engine = create_engine(url_db)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
