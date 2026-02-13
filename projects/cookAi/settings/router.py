from fastapi import APIRouter
from projects.cookAi.routes.cookai_users import router as users_router
from projects.cookAi.routes.recipes import router as recipes_router

cookai_router = APIRouter(prefix="/cookai", tags=["CookAi"])

cookai_router.include_router(users_router, prefix="/users", tags=["CookAi - Users"])
cookai_router.include_router(
    recipes_router, prefix="/recipes", tags=["CookAi - Recipes"]
)
