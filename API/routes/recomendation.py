# API/routes/recommendation.py
from fastapi import APIRouter
from API.models.recomendation import RecommendationInput
from API.services.recomendationsService import RecommendationsService

recomendation_router = APIRouter()

@recomendation_router.post("/recommendation")
def recommend_list(input: RecommendationInput):
    return RecommendationsService.recommend_products(input)