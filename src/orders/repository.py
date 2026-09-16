from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from src.db.models import Order, OrderItem
from decimal import Decimal
import uuid

async def get_order_by_idempotency_key(db: AsyncSession, key: str) -> Order | None:
    stmt = select(Order).where(Order.idempotency_key==key).options(selectinload(Order.items))
    result = await db.scalar(stmt)
    return result

async def create_order(db: AsyncSession, customer_id: uuid.UUID, total: Decimal, idempotency_key: str) -> Order:
    new_order = Order(
        customer_id=customer_id,
        total=total,
        idempotency_key=idempotency_key,
        status='created'
    )
    db.add(new_order)
    await db.flush()
    return new_order

async def create_order_item(db: AsyncSession, order_id: uuid.UUID, product_id: uuid.UUID, quantity: int, price: Decimal) -> OrderItem:
    new_item = OrderItem(
        order_id=order_id,
        product_id=product_id,
        quantity=quantity,
        price=price
    )
    db.add(new_item)
    return new_item

async def read_orders(skip: int, limit: int, db: AsyncSession) -> List[Order]:
    stmt = select(Order)
    orders = await db.scalars(stmt.options(selectinload(Order.items)).offset(skip).limit(limit))
    return orders.all()

async def read_order(order_id: uuid.UUID, db: AsyncSession) -> Order | None:
    stmt = select(Order).where(Order.id == order_id).options(selectinload(Order.items))
    order = await db.scalar(stmt)
    return order