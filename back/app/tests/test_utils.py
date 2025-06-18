import pytest

from app.utils import get_password_hashed, check_password

def test_get_password_hashed():
    password = "hello12345"
    hashed_password = get_password_hashed(password)
    
    assert isinstance(hashed_password, str)
    assert password != hashed_password

def test_check_password():
    password = "hello12345"
    hashed_password = get_password_hashed(password)

    assert check_password(password, hashed_password)