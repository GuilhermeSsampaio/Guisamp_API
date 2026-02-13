from fastapi import FastAPI, APIRouter

from auth.schemas.auth_schema import UserRegister
from projects.cookAi.schemas.cookai_user_schema import CookAiUserResponse

router = APIRouter()

@router.post("/register", response_model=CookAiUserResponse)
# def cookai_register(user_data: UserRegister, session: SessionDep):
    

@router.get("/login")
def cookai_login():
    pass


@router.put("/edit_profile")
def update_profile():
    pass

@router.post("/save_Recipe/{user_id}")
def save_recipe():
    pass

@router.get("my_recipes")
def get_my_recipes():
    pass

@router.put("/update_recipe/{user_id}/{recipe_id}")
def update_recipe():
    pass

@router.delete("/delete_recipe/{user_id}/{recipe_id}")
def delete_recipe():
    pass