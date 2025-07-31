from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI
from database import get_db
from database import SessionLocal
from auth import hash_password
from models.user import User

@asynccontextmanager
async def lifespan(app: FastAPI):
    db: Session = SessionLocal()
    try:
        existing = db.query(User).filter_by(login="admin").first()
        if not existing:
            user = User(login="admin", hashed_password=hash_password("admin"))
            db.add(user)
            db.commit()
            db.refresh(user)
        yield
    finally:
        db.close()
