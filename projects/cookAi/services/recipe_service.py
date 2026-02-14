from uuid import UUID
from sqlmodel import Session

from projects.cookAi.helpers.profile_helpers import get_profile_or_404
from projects.cookAi.helpers.recipe_helpers import check_ownership, get_recipe_or_404
from projects.cookAi.models.recipe import Recipe
from projects.cookAi.repository.recipes_crud import (
    create_recipe,
    delete_recipe,
    list_recipes_by_profile_id,
    update_recipe,
)
from projects.cookAi.schemas.recipe_schema import RecipeRegister, RecipeUpdate


def save_recipe_for_user(session: Session, user_uuid: UUID, recipe_data: RecipeRegister) -> Recipe:
    """Cria uma receita vinculada ao perfil do usuário autenticado."""
    profile = get_profile_or_404(session, user_uuid)

    new_recipe = Recipe(
        title=recipe_data.title,
        content=recipe_data.content,
        font=recipe_data.font,
        link=recipe_data.link,
        cookai_user_id=profile.id,
    )

    return create_recipe(session, new_recipe)


def list_user_recipes(session: Session, user_uuid: UUID) -> list[Recipe]:
    """Lista todas as receitas do usuário autenticado."""
    profile = get_profile_or_404(session, user_uuid)
    return list_recipes_by_profile_id(session, profile.id)


def update_user_recipe(session: Session, user_uuid: UUID, recipe_id: int, data: RecipeUpdate) -> Recipe:
    """Atualiza uma receita. Valida que pertence ao usuário."""
    profile = get_profile_or_404(session, user_uuid)
    recipe = get_recipe_or_404(session, recipe_id)
    check_ownership(recipe, profile.id)

    if data.title is not None:
        recipe.title = data.title
    if data.content is not None:
        recipe.content = data.content

    return update_recipe(session, recipe)


def delete_user_recipe(session: Session, user_uuid: UUID, recipe_id: int) -> str:
    """Exclui uma receita. Valida que pertence ao usuário. Retorna o título."""
    profile = get_profile_or_404(session, user_uuid)
    recipe = get_recipe_or_404(session, recipe_id)
    check_ownership(recipe, profile.id)

    title = recipe.title
    delete_recipe(session, recipe)
    return title
