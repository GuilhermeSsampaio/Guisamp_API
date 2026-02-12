from fastapi import FastAPI, APIRouter

router = APIRouter()

@router.get("/scrap")
def scrap_recipe():
    return {"msg": "scrapping ativo"}