from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from src.orders.schemas import OrderCreate
from fastapi import HTTPException, status
from src.orders import repository as repository_orders
from src.products import repository as repository_products


async def create_order(order_data: OrderCreate, idempotency_key: str, db: AsyncSession):
    
    existing_order  = await repository_orders.get_order_by_idempotency_key(db, idempotency_key)
    if existing_order:
        return existing_order
    
    total = Decimal('0')
    orderitems_data = []
    for item in order_data.items:
        product = await repository_products.read_product_for_update(item.product_id, db)
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')
        
        if product.stock < item.quantity:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Out of stock')
        
        total += product.price * item.quantity
        product.stock -= item.quantity
        orderitems_data.append({
            "product_id": item.product_id,
            "quantity": item.quantity,
            "price": product.price,  
        })
        
    order = await repository_orders.create_order(
        db,
        customer_id=order_data.customer_id,
        total=total,
        idempotency_key=idempotency_key,
    )
    
    for item_data in orderitems_data:
        await repository_orders.create_order_item(
            db,
            order_id=order.id,     
            product_id=item_data["product_id"],   
            quantity=item_data["quantity"],
            price=item_data["price"],
        )
        
    await db.commit()
    return order