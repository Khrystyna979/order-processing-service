from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
import uuid


class ProductCreate(BaseModel):
    
    name: str = Field(min_length=1, max_length=50)
    price: Decimal = Field(gt=0)
    stock: int = Field(ge=0, default=0)
    
    model_config = ConfigDict(str_strip_whitespace=True)

class ProductResponse(BaseModel):
    id: uuid.UUID 
    name: str 
    price: Decimal
    stock: int
    
    model_config = ConfigDict(from_attributes=True)