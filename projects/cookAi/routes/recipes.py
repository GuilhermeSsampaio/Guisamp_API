from fastapi import FastAPI, APIRouter

router = APIRouter()

@router.post("/scrap")
def scrap_recipe():
    return {"msg": "scrapping ativo"}

@router.post("/search_web")
def search_web():
    pass


@router.get("/list")
def list_recipes():
    pass


@router.get("/get_recipe/{recipe_id}")
def get_recipe_by_id():
    pass

