import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, Mapped, relationship
from decimal import Decimal
from sqlalchemy import DateTime, Integer, String, Numeric, ForeignKey, func
from src.db.database import Base
from typing import List
from datetime import datetime

class Product(Base):
    __tablename__ = 'products'
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(50), index=True)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    stock: Mapped[int | None] = mapped_column(Integer, nullable=True)
    order_items: Mapped[List['OrderItem']] = relationship(back_populates='product')

    
class Order(Base):
    __tablename__ = 'orders'
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    total: Mapped[Decimal] = mapped_column(Numeric(10, 2)) 
    status: Mapped[str] = mapped_column(String(20), default="created")
    idempotency_key: Mapped[str] = mapped_column(unique=True) 
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    items: Mapped[List['OrderItem']] = relationship(back_populates='order')
    

class OrderItem(Base):
    __tablename__ = 'orderitems'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('orders.id')) 
    product_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),ForeignKey('products.id'))
    quantity: Mapped[int] = mapped_column(default=1)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    order: Mapped['Order'] = relationship(back_populates='items')
    product: Mapped['Product'] = relationship(back_populates='order_items')