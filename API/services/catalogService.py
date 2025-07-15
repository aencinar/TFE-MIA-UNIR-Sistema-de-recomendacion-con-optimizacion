from API.config.database import collection_name
from pymongo.errors import PyMongoError
from fastapi import HTTPException, status

PAGE_SIZE = 40

class CatalogService:
    @staticmethod
    def get_catalog_filtered(filters):
        try:
            query = {}

            categories = [int(c) for c in filters.get("categories", []) if c not in ("", None)]
            if categories:
                query["category"] = {"$in": categories}

            restrictions = [str(r) for r in filters.get("restrictions", []) if r not in ("", None)]
            if restrictions:
                query["subcategory"] = {"$in": restrictions}

            page = int(filters.get("page", 1))
            if page < 1:
                page = 1
            skip = (page - 1) * PAGE_SIZE

            projection = {
                "_id": 1,  # Si quieres devolver el _id, conviértelo luego
                "supermarket": 1,
                "product_code": 1,
                "category": 1,
                "name": 1,
                "price": 1,
                "lastUpdate": 1,
                "subcategory": 1
            }

            cursor = collection_name.find(query, projection).skip(skip).limit(PAGE_SIZE)
            products = []
            for prod in cursor:
                if "_id" in prod:
                    prod["_id"] = str(prod["_id"])
                products.append(prod)

            total = collection_name.count_documents(query)

            print("QUERY:", query)
            print("PRODUCTOS DEVUELTOS:", len(products))

            return {
                "products": products,
                "total": total,
                "page": page,
                "pages": (total + PAGE_SIZE - 1) // PAGE_SIZE
            }

        except PyMongoError as e:
            print(">>> ERROR AL OBTENER PRODUCTOS:", e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener los productos: {str(e)}"
            )
