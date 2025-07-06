from datetime import datetime, timedelta
from passlib.context import CryptContext
from app.core.config import settings

ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"])

def get_password_hash(pwd: str) -> str:
    return pwd_context.hash(pwd)

def check_password(pwd: str, pwd_db: str) -> bool:
    return pwd_context.verify(pwd, pwd_db)
