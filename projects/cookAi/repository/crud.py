from typing import List
from uuid import UUID
from fastapi import HTTPException
from sqlmodel import select, Session
from projects.cookAi.models.cookai_user import CookAiUser
from projects.cookAi.models.recipe import Recipe
from sqlalchemy.orm import joinedload


def list_cookai_users(session: Session) -> List[CookAiUser]:
    cookai_profiles = session.exec(
        select(CookAiUser).options(joinedload(CookAiUser.user))
    ).all()

    return cookai_profiles


def get_cookai_user_by_id(session: Session, user_uuid: UUID) -> CookAiUser:

    cookai_profile = session.exec(
        select(CookAiUser)
        .options(joinedload(CookAiUser.user))
        .where(CookAiUser.user_id == user_uuid)
    ).first()

    if not cookai_profile:
        raise HTTPException(status_code=404, detail="Perfil Cookai não encontrado")

    return cookai_profile


def list_recipes_by_profile_id(session: Session, profile_id: UUID) -> List[Recipe]:
    recipes = session.exec(
        select(Recipe).where(Recipe.cookai_user_id == profile_id)
    ).all()
    return recipes

def get_recipe_by_id(session: Session, recipe_id: int) -> Recipe:
    recipe = session.get(Recipe, recipe_id)
    
    if not recipe:
        raise HTTPException(status_code=404, detail="Receita não encontrada")
    
    return recipe


def get_or_create_cookai_user(session: Session, user_uuid: UUID) -> CookAiUser:
    """Busca o perfil CookAi pelo user_id. Se não existir, cria automaticamente."""
    cookai_profile = session.exec(
        select(CookAiUser)
        .options(joinedload(CookAiUser.user))
        .where(CookAiUser.user_id == user_uuid)
    ).first()

    if not cookai_profile:
        cookai_profile = CookAiUser(user_id=user_uuid, premium_member=False)
        session.add(cookai_profile)
        session.commit()
        session.refresh(cookai_profile)
        # Carrega o relationship após criação
        cookai_profile = session.exec(
            select(CookAiUser)
            .options(joinedload(CookAiUser.user))
            .where(CookAiUser.id == cookai_profile.id)
        ).first()

    return cookai_profile