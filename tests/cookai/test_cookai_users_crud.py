"""Testes unitários para cookai_users_crud.py — camada pura de dados."""
from uuid import uuid4
from sqlmodel import Session

from auth.models.user import User
from projects.cookAi.models.cookai_user import CookAiUser
from projects.cookAi.repository.cookai_users_crud import (
    create_cookai_user,
    get_cookai_user_by_user_id,
    list_cookai_users,
    update_cookai_user,
)


def _make_user(session: Session) -> User:
    user = User(username=f"u-{uuid4().hex[:6]}", email=f"{uuid4().hex[:6]}@t.com")
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


class TestCreateCookaiUser:
    def test_creates_profile(self, session: Session):
        user = _make_user(session)
        profile = create_cookai_user(session, user.id)

        assert profile is not None
        assert profile.user_id == user.id
        assert profile.premium_member is False

    def test_profile_has_user_relationship(self, session: Session):
        user = _make_user(session)
        profile = create_cookai_user(session, user.id)

        assert profile.user is not None
        assert profile.user.email == user.email


class TestGetCookaiUserByUserId:
    def test_returns_profile(self, session: Session):
        user = _make_user(session)
        create_cookai_user(session, user.id)
        found = get_cookai_user_by_user_id(session, user.id)

        assert found is not None
        assert found.user_id == user.id

    def test_returns_none_if_not_exists(self, session: Session):
        result = get_cookai_user_by_user_id(session, uuid4())
        assert result is None


class TestListCookaiUsers:
    def test_empty(self, session: Session):
        result = list_cookai_users(session)
        assert result == []

    def test_returns_all(self, session: Session):
        for _ in range(3):
            user = _make_user(session)
            create_cookai_user(session, user.id)

        result = list_cookai_users(session)
        assert len(result) == 3


class TestUpdateCookaiUser:
    def test_updates_bios(self, session: Session):
        user = _make_user(session)
        profile = create_cookai_user(session, user.id)
        profile.bios = "Updated bio"

        updated = update_cookai_user(session, profile)
        assert updated.bios == "Updated bio"

    def test_updates_premium(self, session: Session):
        user = _make_user(session)
        profile = create_cookai_user(session, user.id)
        profile.premium_member = True

        updated = update_cookai_user(session, profile)
        assert updated.premium_member is True
