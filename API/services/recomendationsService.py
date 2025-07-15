from fastapi import HTTPException, status
from pymongo.errors import PyMongoError
from AI.service import RecommendationEngine
from API.config.database import collection_name

engine = RecommendationEngine()

class RecommendationsService:
    @staticmethod
    def recommend_products(input):
        try:
            input_codes = [int(p.product_code) for p in input.products]

            restrictions_bin = [
                1 if getattr(input, "lactoseFree", False) else 0,
                1 if getattr(input, "glutenFree", False) else 0,
                1 if getattr(input, "soyFree", False) else 0,
                1 if getattr(input, "vegan", False) else 0,
            ]

            recommended = engine.recommend(
                input_items=input_codes,
                budget=input.budget,
                restrictions=restrictions_bin
            )

            codes_recommended = recommended['recommended_codes']
            codes_str = [int(code) for code in codes_recommended]

            products_cursor = collection_name.find(
                {"product_code": {"$in": codes_str}},
                {"_id": 0}  # Excluir _id si quieres
            )
            products = list(products_cursor)

            product_dict = {p["product_code"]: p for p in products}
            ordered_products = [product_dict[code] for code in codes_str if code in product_dict]

            return {"products": ordered_products}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en recomendación: {str(e)}")