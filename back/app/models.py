from app.core.db import Base

from typing import List
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)


class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[int] = mapped_column(String(50), nullable=False)
    sku: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    ean13: Mapped[str] = mapped_column(String(13), unique=True, nullable=False)
    stock: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    
    history: Mapped[List["StockHistory"]] = relationship(
        "StockHistory", back_populates="item", cascade="all, delete-orphan"
    )


class StockHistory(Base):
    __tablename__ = "stock_history"

    id: Mapped[int] = mapped_column(primary_key=True)
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"))
    prev_stock: Mapped[int] = mapped_column(Integer, nullable=False)
    actual_stock: Mapped[int] = mapped_column(Integer, nullable=False)
    quantity_change: Mapped[int] = mapped_column(Integer, nullable=False)
    move: Mapped[str] = mapped_column(String)

    item: Mapped["Item"] = relationship("Item", back_populates="history")
