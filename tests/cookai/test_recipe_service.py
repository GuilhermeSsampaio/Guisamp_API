"""Testes unitários para recipe_service.py"""
import pytest
from uuid import uuid4
from fastapi import HTTPException
from sqlmodel import Session

from auth.models.user import User
from projects.cookAi.models.cookai_user import CookAiUser
from projects.cookAi.models.recipe import Recipe
from projects.cookAi.services.recipe_service import (
    delete_user_recipe,
    list_user_recipes,
    save_recipe_for_user,
    update_user_recipe,
)
from projects.cookAi.schemas.recipe_schema import RecipeRegister, RecipeUpdate


def _make_profile(session: Session) -> CookAiUser:
    """Helper: cria User + CookAiUser."""
    user = User(username=f"u-{uuid4().hex[:6]}", email=f"{uuid4().hex[:6]}@t.com")
    session.add(user)
    session.commit()
    session.refresh(user)

    profile = CookAiUser(user_id=user.id, premium_member=False)
    session.add(profile)
    session.commit()
    session.refresh(profile)
    return profile


def _make_recipe_data(title="Bolo", content="Conteúdo") -> RecipeRegister:
    return RecipeRegister(title=title, content=content, font="fonte", link="link")
    def test_creates_recipe(self, session: Session):
        profile = _make_profile(session)
        data = _make_recipe_data()
        recipe = save_recipe_for_user(session, profile.user_id, data)

        assert recipe.title == "Bolo"
        assert recipe.cookai_user_id == profile.id

    def test_raises_404_no_profile(self, session: Session):
        data = _make_recipe_data("X", "Y")
        with pytest.raises(HTTPException) as exc:
            save_recipe_for_user(session, uuid4(), data)
        assert exc.value.status_code == 404


class TestListUserRecipes:
    def test_empty_list(self, session: Session):
        profile = _make_profile(session)
        result = list_user_recipes(session, profile.user_id)
        assert result == []

    def test_returns_user_recipes(self, session: Session):
        profile = _make_profile(session)
        save_recipe_for_user(session, profile.user_id, _make_recipe_data("R1", "C1"))
        save_recipe_for_user(session, profile.user_id, _make_recipe_data("R2", "C2"))

        result = list_user_recipes(session, profile.user_id)
        assert len(result) == 2

    def test_not_mixed_between_users(self, session: Session):
        p1 = _make_profile(session)
        p2 = _make_profile(session)
        save_recipe_for_user(session, p1.user_id, _make_recipe_data("P1R", "c"))
        save_recipe_for_user(session, p2.user_id, _make_recipe_data("P2R", "c"))

        assert len(list_user_recipes(session, p1.user_id)) == 1
        assert len(list_user_recipes(session, p2.user_id)) == 1


class TestUpdateUserRecipe:
    def test_updates_title(self, session: Session):
        profile = _make_profile(session)
        recipe = save_recipe_for_user(
            session, profile.user_id, _make_recipe_data("Old", "c")
        )
        updated = update_user_recipe(
            session, profile.user_id, recipe.id, RecipeUpdate(title="New")
        )
        assert updated.title == "New"
        assert updated.content == "c"  # não alterou

    def test_updates_content(self, session: Session):
        profile = _make_profile(session)
        recipe = save_recipe_for_user(
            session, profile.user_id, _make_recipe_data("T", "Old")
        )
        updated = update_user_recipe(
            session, profile.user_id, recipe.id, RecipeUpdate(content="New")
        )
        assert updated.content == "New"

    def test_raises_404_recipe_not_found(self, session: Session):
        profile = _make_profile(session)
        with pytest.raises(HTTPException) as exc:
            update_user_recipe(session, profile.user_id, 99999, RecipeUpdate(title="X"))
        assert exc.value.status_code == 404

    def test_raises_403_not_owner(self, session: Session):
        owner = _make_profile(session)
        other = _make_profile(session)
        recipe = save_recipe_for_user(
            session, owner.user_id, _make_recipe_data("Mine", "c")
        )
        with pytest.raises(HTTPException) as exc:
            update_user_recipe(session, other.user_id, recipe.id, RecipeUpdate(title="Hack"))
        assert exc.value.status_code == 403


class TestDeleteUserRecipe:
    def test_deletes_recipe(self, session: Session):
        profile = _make_profile(session)
        recipe = save_recipe_for_user(
            session, profile.user_id, _make_recipe_data("Del", "c")
        )
        title = delete_user_recipe(session, profile.user_id, recipe.id)
        assert title == "Del"
        assert list_user_recipes(session, profile.user_id) == []

    def test_raises_404_not_found(self, session: Session):
        profile = _make_profile(session)
        with pytest.raises(HTTPException) as exc:
            delete_user_recipe(session, profile.user_id, 99999)
        assert exc.value.status_code == 404

    def test_raises_403_not_owner(self, session: Session):
        owner = _make_profile(session)
        other = _make_profile(session)
        recipe = save_recipe_for_user(
            session, owner.user_id, _make_recipe_data("T", "c")
        )
        with pytest.raises(HTTPException) as exc:
            delete_user_recipe(session, other.user_id, recipe.id)
        assert exc.value.status_code == 403
