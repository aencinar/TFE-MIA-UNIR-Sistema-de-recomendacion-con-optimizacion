from fastapi import APIRouter
from routes.product import product_router

router = APIRouter()

@router.get("/")
def health_check():
    return 'Health check complete'

router.include_router(product_router, prefix="/api")