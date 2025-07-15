from fastapi import APIRouter, status, Query
from fastapi import Path
from API.models.catalog import CatalogFilters
from API.services.catalogService import CatalogService

catalog_router = APIRouter()

@catalog_router.get("/catalog", status_code=status.HTTP_200_OK)
def get_catalog(
    page: int = Query(1, ge=1),
    categories: list[int] = Query([]),
    restrictions: list[str] = Query([])
):
    filters = {
        "page": page,
        "categories": categories,
        "restrictions": restrictions
    }
    return CatalogService.get_catalog_filtered(filters)


