from typing import List
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.db.models import Product
from src.products.schemas import ProductCreate

async def read_products(skip: int, limit: int, db: AsyncSession) -> List[Product]:
    stmt = select(Product)
    products = await db.scalars(stmt.offset(skip).limit(limit))
    return products.all()

async def read_product(product_id: uuid.UUID, db: AsyncSession) -> Product | None:
    stmt = select(Product).where(Product.id==product_id)
    product = await db.scalar(stmt)
    return product

async def create_product(body: ProductCreate, db: AsyncSession) -> Product:
    new_product = Product(**body.model_dump())
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    return new_product