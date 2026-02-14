from typing import List
from fastapi import Depends, APIRouter
from uuid import UUID

from auth.schemas.auth_schema import UserLogin, UserRegister
from auth.schemas.token_schema import TokenResponse
from auth.security.dependencies import current_user
from config.db import SessionDep

from projects.cookAi.schemas.cookai_user_schema import (
    CookAiUserResponse,
    CookAiUserUpdate,
)
from projects.cookAi.schemas.recipe_schema import (
    RecipeRegister,
    RecipeResponse,
    RecipeUpdate,
)

from projects.cookAi.services.user_service import (
    authenticate_cookai_user,
    edit_profile,
    get_my_profile,
    list_all_cookai_users,
    register_cookai_user,
)
from projects.cookAi.services.recipe_service import (
    delete_user_recipe,
    list_user_recipes,
    save_recipe_for_user,
    update_user_recipe,
)

router = APIRouter()


# ── Auth ────────────────────────────────────────────────────


@router.post("/register", response_model=CookAiUserResponse)
def cookai_user_register(user_data: UserRegister, session: SessionDep):
    return register_cookai_user(session, user_data)


@router.post("/login", response_model=TokenResponse)
def cookai_login(login_data: UserLogin, session: SessionDep):
    token = authenticate_cookai_user(session, login_data.email, login_data.password)
    return {"access_token": token, "token_type": "bearer"}


# ── Perfil ──────────────────────────────────────────────────


@router.get("/list_cookai_users", response_model=List[CookAiUserResponse])
def get_cookai_users(session: SessionDep):
    return list_all_cookai_users(session)


@router.get("/me", response_model=CookAiUserResponse)
def me(session: SessionDep, user_id: str = Depends(current_user)):
    return get_my_profile(session, UUID(user_id))


@router.put("/edit_profile", response_model=CookAiUserResponse)
def update_profile(
    updates: CookAiUserUpdate,
    session: SessionDep,
    user_id: str = Depends(current_user),
):
    return edit_profile(session, UUID(user_id), updates)


# ── Receitas ────────────────────────────────────────────────


@router.post("/save_recipe", response_model=RecipeResponse)
def save_recipe(
    recipe_data: RecipeRegister,
    session: SessionDep,
    user_id: str = Depends(current_user),
):
    return save_recipe_for_user(session, UUID(user_id), recipe_data)


@router.get("/my_recipes", response_model=List[RecipeResponse])
def get_my_recipes(session: SessionDep, user_id: str = Depends(current_user)):
    return list_user_recipes(session, UUID(user_id))


@router.put("/update_recipe/{recipe_id}", response_model=RecipeResponse)
def update_recipe(
    recipe_data: RecipeUpdate,
    session: SessionDep,
    recipe_id: int,
    user_id: str = Depends(current_user),
):
    return update_user_recipe(session, UUID(user_id), recipe_id, recipe_data)


@router.delete("/delete_recipe/{recipe_id}")
def delete_recipe(
    session: SessionDep,
    recipe_id: int,
    user_id: str = Depends(current_user),
):
    title = delete_user_recipe(session, UUID(user_id), recipe_id)
    return {"message": f"Receita {title} excluída com sucesso"}
