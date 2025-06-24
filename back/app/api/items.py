from typing import List
from fastapi import APIRouter,  HTTPException

from app.core.db import SessionDep
from app.schemas import ItemBase, StockHistoryBase, \
                        StockUpdateRequest
from app.crud import item as crud
from app.crud.item import DuplicateItemError

router = APIRouter(prefix="/items", tags=['items'])

@router.get("/", response_model=List[ItemBase])
async def list_items(session: SessionDep):
    items = await crud.get_items(session)
    return items

@router.get("/history", response_model=List[StockHistoryBase])
async def list_histories(session: SessionDep):
    histories = await crud.get_histories_stock(session)
    return histories

@router.post("/", status_code=201)
async def create_item(session: SessionDep, item_in: ItemBase):
    try:
        item = await crud.create_item(session, item_in)
    except DuplicateItemError as e:
        raise HTTPException(status_code=401, detail=f"Valor {e} ya existe.")
    return {
        "msg": "Item creado correctamente.",
        "data": item
    }

@router.patch("/{item_id}/stock", status_code=200)
async def update_stock(session: SessionDep, item_id: int, data:StockUpdateRequest):
    try:
        item = await crud.get_item_by_id(session, item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Item no encontrado.")
        if data.new_stock < 0:
            raise HTTPException(status_code=400, detail="El stock no puede ser negativo.")
        movement = await crud.update_item_stock(session, item, data.new_stock)
        # await session.refresh()
        return {
            "msg":"Stock actualizado correctamente.",
            "data":movement
        }
    except HTTPException:
        raise
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al actualizar stock: {str(e)}"
        )
