from API.config.database import collection_name
from bson import ObjectId
from API.schema.schemas import list_serial
from API.models.product import Product
from pymongo.errors import PyMongoError
from fastapi import HTTPException, status

class ProductService:

    @staticmethod
    def get_all_products():
        try:
            products = list_serial(collection_name.find())
            return products
        except PyMongoError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener los productos: {str(e)}"
            )

    @staticmethod
    def create_product(product: Product):
        try:
            result = collection_name.insert_one(product.dict())
            return {"message": "Producto creado", "id": str(result.inserted_id)}
        except PyMongoError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al crear el producto: {str(e)}"
            )
        
    
    @staticmethod
    def update_product_price(product_id: str, new_price: float):
        try:
            if not ObjectId.is_valid(product_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="ID no válido"
                )
            if new_price <= 0:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="El precio debe ser mayor a 0"
                )

            result = collection_name.update_one(
                {"_id": ObjectId(product_id)},
                {"$set": {"price": new_price}}
            )

            if result.matched_count == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Producto no encontrado"
                )

            return {"message": "Precio actualizado correctamente"}

        except PyMongoError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al actualizar el producto: {str(e)}"
            )