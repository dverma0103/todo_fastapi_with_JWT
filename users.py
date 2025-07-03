from passlib.context import CryptContext
from sqlalchemy.orm import Session
from models import User, UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

def get_user(db:Session, email:str):
    return db.query(User).filter(User.email == email).first()

def create_user(db:Session, user:UserCreate):
    hashed_pass = pwd_context.hash(user.password)
    user_db = User(name = user.name, email = user.email, hashed_password = hashed_pass)
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db

def authenticate_user(db:Session, username:str, password:str):
    user = get_user(db, username)
    if not user:
        return None
    return user