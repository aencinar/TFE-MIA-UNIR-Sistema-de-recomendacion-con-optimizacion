from pydantic import BaseModel
from typing import List, Optional

class CatalogFilters(BaseModel):
    categories: Optional[List[int]] = []
    restrictions: Optional[List[str]] = []
    page: Optional[int] = 1