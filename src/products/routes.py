from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from src.db.database import get_db
from src.products.schemas import ProductCreate, ProductResponse
from src.products import repository as repository_products
import uuid


router = APIRouter(prefix='/products', tags=["products"])

@router.get('/', response_model=List[ProductResponse])
async def read_products(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    products = await repository_products.read_products(skip, limit, db)
    return products
    
@router.get('/{product_id}', response_model=ProductResponse)
async def read_product(product_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    product = await repository_products.read_product(product_id, db)
    if product:
        return product
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')
    
@router.post('/', response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(body: ProductCreate, db: AsyncSession = Depends(get_db)):
    product = await repository_products.create_product(body, db)
    return product