from typing import List, Optional
from uuid import UUID
from sqlmodel import select, Session

from projects.cookAi.models.recipe import Recipe


def get_recipe_by_id(session: Session, recipe_id: int) -> Optional[Recipe]:
    """Retorna a receita pelo id ou None."""
    return session.get(Recipe, recipe_id)


def list_recipes_by_profile_id(session: Session, profile_id: UUID) -> List[Recipe]:
    return session.exec(select(Recipe).where(Recipe.cookai_user_id == profile_id)).all()


def create_recipe(session: Session, recipe: Recipe) -> Recipe:
    session.add(recipe)
    session.commit()
    session.refresh(recipe)
    return recipe


def update_recipe(session: Session, recipe: Recipe) -> Recipe:
    session.add(recipe)
    session.commit()
    session.refresh(recipe)
    return recipe


def delete_recipe(session: Session, recipe: Recipe) -> None:
    session.delete(recipe)
    session.commit()
