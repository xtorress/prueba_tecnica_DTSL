from pydantic import BaseModel, Field, EmailStr

# Base User schema.
class UserBase(BaseModel):
    username: str = Field(max_length=50)
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(min_length=8)


# Base Item schema.
class ItemBase(BaseModel):
    sku: str = Field(min_length=1, max_length=50)
    ean13: str = Field(min_length=13, max_length=13)
    stock: int = Field(ge=0)


class Item(ItemBase):
    id: int
