from fastapi import FastAPI, APIRouter

from config.db import SessionDep
from projects.cookAi.schemas.recipe_schema import RecipeResponse
from projects.cookAi.services.web_search import search_recipes_from_web

router = APIRouter()

@router.post("/scrap", response_model=RecipeResponse)
def scrap_recipe(url:str):
    scrapping_result = scrap_recipe(url)
    return scrapping_result

@router.post("/search_web")
def search_web(query):
    recipes = search_recipes_from_web(query)
    return recipes


# futuramente se user desejar, pode deixar a receita pública e assim outros poderiam ver
@router.get("/list_public_recipes")
def list_public_recipes():
    pass



