import pytest
from pydantic import ValidationError

from app.schemas import UserBase, UserCreate, Item, ItemBase

@pytest.fixture
def user():
    return {
        "username": "Luis Enrique",
        "email": "luis@gmail.com",
        "password": "12345678"
    }

@pytest.fixture()
def item():
    return {
        "sku": "camisa-azul-m",
        "ean13": "1234567891234",
        "stock": 13
    }

###### User tests.

def test_user_create_valid(user):
    new_user = UserCreate(**user)
    assert new_user.username == "Luis Enrique"

def test_user_create_invalid_emai(user):
    user['email'] = "luis@1"
    with pytest.raises(ValidationError):
        UserCreate(**user)

def test_user_create_invalid_password(user):
    user['password'] = "12345"
    with pytest.raises(ValidationError):
        UserCreate(**user)

###### Item tests.

def test_item_valid(item):
    item1 = ItemBase(**item)
    assert item1.sku == "camisa-azul-m"

def test_item_stock_invalid(item):
    item['stock'] = -1
    with pytest.raises(ValidationError):
        ItemBase(**item)