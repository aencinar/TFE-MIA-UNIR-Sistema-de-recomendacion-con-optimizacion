from fastapi import APIRouter, status, Path
from models.product import Product
from services.productService import ProductService

product_router = APIRouter()

@product_router.get("/products", status_code=status.HTTP_200_OK)
async def get_products():
    return ProductService.get_all_products()

@product_router.post("/saveProduct", status_code=status.HTTP_201_CREATED)
async def post_product(product: Product):
    return ProductService.create_product(product)

@product_router.put("/updatePrice/{product_id}", status_code=status.HTTP_200_OK)
async def update_price(product_id: str, new_price: float = Path(..., gt=0)):
    return ProductService.update_product_price(product_id, new_price)
