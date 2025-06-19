import pytest
from app.models import Item, User
from app.schemas import StockUpdateRequest

@pytest.mark.asyncio
async def test_list_items_empty(client):
    response = await client.get("/items/")
    assert response.status_code == 200
    assert response.json() == []

@pytest.mark.asyncio
async def test_list_items(client, async_session):
    item = Item(name="TestItem", sku="SKU1", ean13="1234567890123", stock=10)
    async_session.add(item)
    item2 = Item(name="TestItem2", sku="SKU2", ean13="2234567890123", stock=20)
    async_session.add(item2)
    await async_session.commit()
    await async_session.refresh(item)
    await async_session.refresh(item2)
    response = await client.get("/items/")
    assert response.status_code == 200
    assert len(response.json()) == 2

@pytest.mark.asyncio
async def test_update_stock(client, async_session):
    # Crear un item de prueba
    item = Item(name="TestItem", sku="SKU1", ean13="1234567890123", stock=10)
    async_session.add(item)
    await async_session.commit()
    await async_session.refresh(item)

    payload = {"new_stock": 20}
    response = await client.patch(f"/items/{item.id}/stock", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["msg"] == "Stock actualizado correctamente."
    assert data["data"]["actual_stock"] == 20
    assert data["data"]["prev_stock"] == 10
    assert data["data"]["move"] == "entrada"

@pytest.mark.asyncio
async def test_update_stock_negative(client, async_session):
    item = Item(name="Negativo", sku="NEG1", ean13="9999999999999", stock=5)
    async_session.add(item)
    await async_session.commit()
    await async_session.refresh(item)

    payload = {"new_stock": -5}
    response = await client.patch(f"/items/{item.id}/stock", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "El stock no puede ser negativo."

@pytest.mark.asyncio
async def test_list_histories(client, async_session):
    response = await client.get("/items/history")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


## User test.

@pytest.mark.asyncio
async def test_create_user_success(client, async_session):
    payload = {
        "email": "test@example.com",
        "username": "Test User",
        "password": "strongpassword"
    }

    response = await client.post("/users/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["msg"] == "Usuario creado correctamente."
    assert data["data"]["email"] == payload["email"]
