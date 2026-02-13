from fastapi import FastAPI, APIRouter

from config.db import SessionDep

router = APIRouter()

@router.post("/scrap")
def scrap_recipe():
    return {"msg": "scrapping ativo"}

@router.post("/search_web")
def search_web():
    pass


@router.get("/list_public_recipes")
def list_public_recipes():
    pass



