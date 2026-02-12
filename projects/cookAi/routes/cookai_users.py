from fastapi import FastAPI, APIRouter

router = APIRouter()

@router.get("/cookai_teste")
def teste():
    return {"msg": "cookaiuser ativo"}