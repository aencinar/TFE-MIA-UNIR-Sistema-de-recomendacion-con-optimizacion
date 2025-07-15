from pydantic import BaseModel, Field
from typing import Optional

class Product(BaseModel):
    product_code: str = Field(..., min_length=1)
    supermarket: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    category: str = Field(..., min_length=1)
    subcategory: str = Field(..., min_length=1)
    price: float = Field(..., gt=0)
    lastUpdate: int = Field(..., gt=0)