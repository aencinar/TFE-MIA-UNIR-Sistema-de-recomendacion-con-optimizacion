from typing import List, Optional
from pydantic import BaseModel

class ProductInput(BaseModel):
    _id: str
    product_code: str
    name: str

class RecommendationInput(BaseModel):
    products: List[ProductInput]
    budget: float
    lactoseFree: Optional[bool] = False
    glutenFree: Optional[bool] = False
    soyFree: Optional[bool] = False
    vegan: Optional[bool] = False
