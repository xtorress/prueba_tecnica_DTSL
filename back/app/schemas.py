from pydantic import BaseModel, Field, EmailStr

# Base User schema.
class UserBase(BaseModel):
    username: str = Field(max_length=50)
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(min_length=8)


# Base Item schema.
class ItemBase(BaseModel):
    name: str = Field(max_length=50)
    sku: str = Field(min_length=1, max_length=50)
    ean13: str = Field(min_length=13, max_length=13)
    stock: int = Field(ge=0)


class ItemSchema(ItemBase):
    id: int


# Base Stock History schema.
class StockHistoryBase(BaseModel):
    prev_stock: int
    actual_stock: int
    quantity_change: int
    move: str
    item: ItemSchema

    class Config:
        from_attributes = True


class StockHistorySchema(StockHistoryBase):
    id: int


class StockUpdateRequest(BaseModel):
    new_stock: int


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    sub: EmailStr | None = None