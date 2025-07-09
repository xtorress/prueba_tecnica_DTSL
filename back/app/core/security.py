from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from app.core.config import settings

import jwt

ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"])

def create_token(subject: str, expire_delta: timedelta) -> str:
    expire = datetime.now(timezone.utc) + expire_delta
    to_encoded = {"exp": expire, "sub": subject}
    encoded_jwt = jwt.encode(to_encoded, settings.SECRET_KEY, ALGORITHM)
    return encoded_jwt

def get_password_hash(pwd: str) -> str:
    return pwd_context.hash(pwd)

def check_password(pwd: str, pwd_db: str) -> bool:
    return pwd_context.verify(pwd, pwd_db)
