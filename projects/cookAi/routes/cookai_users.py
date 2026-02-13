from typing import List
from fastapi import Depends, APIRouter, HTTPException, status
from uuid import UUID

from auth.models.auth_provider import AuthProvider
from auth.models.user import User
from auth.schemas.auth_schema import UserLogin, UserRegister
from auth.schemas.token_schema import TokenResponse
from auth.security.dependencies import current_user
from auth.security.hashing import hash_password
from auth.services.auth_service import login_user
from config.db import SessionDep

from projects.cookAi.models.cookai_user import CookAiUser
from projects.cookAi.models.recipe import Recipe
from projects.cookAi.repository.crud import (
    get_cookai_user_by_id,
    list_cookai_users,
    list_recipes_by_profile_id,
)
from projects.cookAi.schemas.cookai_user_schema import (
    CookAiUserResponse,
    CookAiUserUpdate,
)
from projects.cookAi.schemas.recipe_schema import RecipeRegister, RecipeResponse

router = APIRouter()


@router.post("/register", response_model=CookAiUserResponse)
def cookai_user_register(user_data: UserRegister, session: SessionDep):

    user_base = User(
        username=user_data.username,
        email=user_data.email,
    )

    session.add(user_base)
    session.commit()
    session.refresh(user_base)

    auth_provider = AuthProvider(
        user_id=user_base.id,
        provider="local",
        password_hash=hash_password(user_data.password),
    )

    session.add(auth_provider)
    session.commit()

    cookai_user = CookAiUser(user_id=user_base.id, premium_member=False)
    session.add(cookai_user)
    session.commit()
    session.refresh(cookai_user)

    return CookAiUserResponse(
        id=cookai_user.id,
        username=user_base.username,
        email=user_base.email,
        user_id=user_base.id,
        bios=cookai_user.bios,
        premium_member=cookai_user.premium_member,
    )


@router.post("/login", response_model=TokenResponse)
def cookai_login(login_data: UserLogin, session: SessionDep):
    """
    Realiza login reutilizando o núcleo de autenticação.
    Retorna o Token JWT padrão.
    """
    token = login_user(session, login_data.email, login_data.password)

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas"
        )

    return {"access_token": token, "token_type": "bearer"}


@router.get("/list_cookai_users", response_model=List[CookAiUserResponse])
def get_cookai_users(session: SessionDep):
    # faz uma única consulta e traz todos

    cookai_profiles = list_cookai_users(session)

    results = []

    for profile in cookai_profiles:
        results.append(
            CookAiUserResponse(
                id=profile.id,
                user_id=profile.user.id,
                username=profile.user.username,
                email=profile.user.email,
                bios=profile.bios,
                premium_member=profile.premium_member,
            )
        )

    return results


@router.put("/edit_profile", response_model=CookAiUserResponse)
def update_profile(
    updates: CookAiUserUpdate, session: SessionDep, user_id: str = Depends(current_user)
):
    # 1. Converta o ID de string para UUID
    user_uuid = UUID(user_id)

    cookai_user_profile = get_cookai_user_by_id(session, user_uuid)

    if not cookai_user_profile:
        raise HTTPException(status_code=404, detail="Perfil CookAi não encontrado")

    if updates.bios is not None:
        cookai_user_profile.bios = updates.bios

    session.add(cookai_user_profile)
    session.commit()
    session.refresh(cookai_user_profile)

    return CookAiUserResponse(
        id=cookai_user_profile.id,
        user_id=cookai_user_profile.user_id,
        username=cookai_user_profile.user.username,
        email=cookai_user_profile.user.email,
        bios=cookai_user_profile.bios,
        premium_member=cookai_user_profile.premium_member,
    )


@router.post("/save_Recipe", response_model=RecipeResponse)
def save_recipe(
    recipe_data: RecipeRegister,
    session: SessionDep,
    user_id: str = Depends(current_user),
):

    user_uuid = UUID(user_id)

    cook_ai_profile = get_cookai_user_by_id(session, user_uuid)

    new_recipe = Recipe(
        title=recipe_data.title,
        content=recipe_data.content,
        font=recipe_data.font,
        link=recipe_data.link,
        cookai_user_id=cook_ai_profile.id,
    )

    session.add(new_recipe)
    session.commit()
    session.refresh(new_recipe)

    return new_recipe


@router.get("/my_recipes", response_model=List[RecipeResponse])
def get_my_recipes(session: SessionDep, user_id: str = Depends(current_user)):

    user_uuid = UUID(user_id)
    cookai_profile = get_cookai_user_by_id(session, user_uuid)

    recipes = list_recipes_by_profile_id(session, cookai_profile.id)
    return recipes


@router.put("/update_recipe/{recipe_id}", response_model=RecipeResponse)
def update_recipe(session: SessionDep, user_id: str = Depends(current_user)):
    pass


@router.delete("/delete_recipe/{recipe_id}")
def delete_recipe(session: SessionDep, user_id: str = Depends(current_user)):
    pass
