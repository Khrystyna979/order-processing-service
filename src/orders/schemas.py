from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
import uuid
from typing import List
from datetime import datetime

class OrderItemCreate(BaseModel):
    
    product_id: uuid.UUID
    quantity: int = Field(gt=0, default=1)
    
    model_config = ConfigDict(str_strip_whitespace=True)
    
class OrderCreate(BaseModel):
    
    customer_id: uuid.UUID
    items: List[OrderItemCreate] = Field(min_length=1)
    
    model_config = ConfigDict(str_strip_whitespace=True)
    
class OrderItemResponse(OrderItemCreate):
    
    id: uuid.UUID
    order_id: uuid.UUID
    price: Decimal
    
    model_config = ConfigDict(from_attributes=True)
    
class OrderResponse(OrderCreate):
    
    id: uuid.UUID
    items: List[OrderItemResponse]
    total: Decimal = Field(gt=0)
    status: str = Field(min_length=1, max_length=20, default="created")
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)