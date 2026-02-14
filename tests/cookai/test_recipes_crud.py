"""Testes unitários para recipes_crud.py — camada pura de dados."""
from uuid import uuid4
from sqlmodel import Session

from auth.models.user import User
from projects.cookAi.models.cookai_user import CookAiUser
from projects.cookAi.models.recipe import Recipe
from projects.cookAi.repository.recipes_crud import (
    create_recipe,
    delete_recipe,
    get_recipe_by_id,
    list_recipes_by_profile_id,
    update_recipe,
)


def _make_profile(session: Session) -> CookAiUser:
    user = User(username=f"u-{uuid4().hex[:6]}", email=f"{uuid4().hex[:6]}@t.com")
    session.add(user)
    session.commit()
    session.refresh(user)

    profile = CookAiUser(user_id=user.id, premium_member=False)
    session.add(profile)
    session.commit()
    session.refresh(profile)
    return profile


def _make_recipe(session: Session, profile: CookAiUser, title: str = "Test") -> Recipe:
    recipe = Recipe(
        title=title,
        content="content",
        font="font",
        link="link",
        cookai_user_id=profile.id,
    )
    return create_recipe(session, recipe)


class TestCreateRecipe:
    def test_creates_and_returns(self, session: Session):
        profile = _make_profile(session)
        recipe = _make_recipe(session, profile, "Bolo")

        assert recipe.id is not None
        assert recipe.title == "Bolo"
        assert recipe.cookai_user_id == profile.id


class TestGetRecipeById:
    def test_found(self, session: Session):
        profile = _make_profile(session)
        recipe = _make_recipe(session, profile)

        found = get_recipe_by_id(session, recipe.id)
        assert found is not None
        assert found.id == recipe.id

    def test_not_found(self, session: Session):
        result = get_recipe_by_id(session, 99999)
        assert result is None


class TestListRecipesByProfileId:
    def test_empty(self, session: Session):
        profile = _make_profile(session)
        result = list_recipes_by_profile_id(session, profile.id)
        assert result == []

    def test_filters_by_profile(self, session: Session):
        p1 = _make_profile(session)
        p2 = _make_profile(session)

        _make_recipe(session, p1, "R1")
        _make_recipe(session, p1, "R2")
        _make_recipe(session, p2, "R3")

        result_p1 = list_recipes_by_profile_id(session, p1.id)
        result_p2 = list_recipes_by_profile_id(session, p2.id)

        assert len(result_p1) == 2
        assert len(result_p2) == 1


class TestUpdateRecipe:
    def test_updates_fields(self, session: Session):
        profile = _make_profile(session)
        recipe = _make_recipe(session, profile)

        recipe.title = "Updated"
        recipe.content = "New content"
        updated = update_recipe(session, recipe)

        assert updated.title == "Updated"
        assert updated.content == "New content"


class TestDeleteRecipe:
    def test_removes_from_db(self, session: Session):
        profile = _make_profile(session)
        recipe = _make_recipe(session, profile)
        recipe_id = recipe.id

        delete_recipe(session, recipe)
        assert get_recipe_by_id(session, recipe_id) is None
