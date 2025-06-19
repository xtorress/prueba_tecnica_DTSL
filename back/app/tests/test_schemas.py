import pytest
from pydantic import ValidationError

from app.schemas import UserBase, UserCreate, ItemSchema, ItemBase, \
                    StockHistorySchema, StockHistoryBase

@pytest.fixture
def user():
    return {
        "username": "Luis Enrique",
        "email": "luis@gmail.com",
        "password": "12345678"
    }

@pytest.fixture
def item():
    return {
        "name": "camisa azul",
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


###### StockHistory tests.

def test_stock_history_base():
    item = ItemSchema(id=1, 
                name="camisa azul", 
                sku="camisa-azul-m", 
                ean13="1234567891234", 
                stock=13
    )
    data = {
        "prev_stock": 10,
        "actual_stock": 5,
        "quantity_change": -5,
        "move": "sale",
        "item": item
    }
    history = StockHistoryBase(**data)
    assert history.prev_stock == 10
    assert history.actual_stock == 5
    assert history.quantity_change == -5
    assert history.move == "sale"
    assert history.item.id == 1

def test_stock_history_requires_id():
    item = ItemSchema(id=1, 
                name="camisa azul", 
                sku="camisa-azul-m", 
                ean13="1234567891234", 
                stock=13
    )
    data = {
        "prev_stock": 10,
        "actual_stock": 5,
        "quantity_change": -5,
        "move": "sale",
        "item": item,
        "id": 100
    }
    history = StockHistorySchema(**data)
    assert history.id == 100