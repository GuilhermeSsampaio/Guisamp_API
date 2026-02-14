from uuid import UUID
from fastapi import HTTPException, status
from sqlmodel import Session

from projects.cookAi.models.recipe import Recipe
from projects.cookAi.repository.recipes_crud import get_recipe_by_id


def get_recipe_or_404(session: Session, recipe_id: int) -> Recipe:
    """Busca receita pelo id ou lança 404."""
    recipe = get_recipe_by_id(session, recipe_id)

    if not recipe:
        raise HTTPException(status_code=404, detail="Receita não encontrada")

    return recipe


def check_ownership(recipe: Recipe, profile_id: UUID) -> None:
    """Valida que a receita pertence ao perfil. Lança 403 se não pertencer."""
    if recipe.cookai_user_id != profile_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não possui permissão para esta receita",
        )
