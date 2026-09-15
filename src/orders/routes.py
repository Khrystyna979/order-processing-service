from fastapi import APIRouter, HTTPException, Depends, Header, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from src.db.database import get_db
from src.orders.schemas import OrderCreate, OrderResponse, OrderItemCreate, OrderItemResponse
from src.orders import repository as repository_orders
import uuid
from src.orders import service as service_orders

router = APIRouter(prefix='/orders', tags=["orders"])

@router.get('/', response_model=List[OrderResponse])
async def read_orders(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    orders = await repository_orders.read_orders(skip, limit, db)
    return orders
    
@router.get('/{order_id}', response_model=OrderResponse)
async def read_order(order_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    order = await repository_orders.read_order(order_id, db)
    if order:
        return order
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Order not found')
    
@router.post('/', response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(body: OrderCreate, idempotency_key: str = Header(...), db: AsyncSession = Depends(get_db)):
    order = await service_orders.create_order(body, idempotency_key, db)
    return order
    

    