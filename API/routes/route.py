from fastapi import APIRouter
from API.routes.product import product_router
from API.routes.recomendation import recomendation_router
from API.routes.catalog import catalog_router

router = APIRouter()

@router.get("/")
def health_check():
    return 'Health check complete'

router.include_router(product_router, prefix="/api")
router.include_router(recomendation_router, prefix="/api")
router.include_router(catalog_router, prefix="/api")