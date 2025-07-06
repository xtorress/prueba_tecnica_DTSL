import pytest

from app.core.security import get_password_hash, check_password

def test_get_password_hashed():
    password = "hello12345"
    hashed_password = get_password_hash(password)
    
    assert isinstance(hashed_password, str)
    assert password != hashed_password

def test_check_password():
    password = "hello12345"
    hashed_password = get_password_hash(password)

    assert check_password(password, hashed_password)