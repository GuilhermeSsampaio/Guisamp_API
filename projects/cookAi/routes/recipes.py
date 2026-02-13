from typing import List
from fastapi import FastAPI, APIRouter

from config.db import SessionDep
from projects.cookAi.schemas.recipe_schema import RecipeResponse, ScrappingResponse
from projects.cookAi.services.scrapping import scrap_recipe
from projects.cookAi.services.web_search import search_recipes_from_web

router = APIRouter()


@router.post("/scrap", response_model=ScrappingResponse)
def scraper_recipes(url: str):
    scrapping_result = scrap_recipe(url)
    return scrapping_result


@router.post("/search_web", response_model=List[ScrappingResponse])
def search_web(query: str):
    recipes = search_recipes_from_web(query)
    return recipes


# futuramente se user desejar, pode deixar a receita pública e assim outros poderiam ver
@router.get("/list_public_recipes")
def list_public_recipes():
    pass
