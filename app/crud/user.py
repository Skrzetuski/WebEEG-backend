from sqlalchemy.orm import Session
from models.user import User
from auth import hash_password

def get_user_by_login(db: Session, login: str):
    return db.query(User).filter(User.login == login).first()

def create_user(db: Session, login: str, password: str):
    db_user = User(login=login, hashed_password=hash_password(password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
