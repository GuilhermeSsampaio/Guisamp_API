"""Testes unitários para user_service.py"""
import pytest
from uuid import uuid4
from fastapi import HTTPException
from sqlmodel import Session, select

from auth.models.user import User
from auth.models.auth_provider import AuthProvider
from auth.security.hashing import hash_password

from projects.cookAi.models.cookai_user import CookAiUser
from projects.cookAi.services.user_service import (
    authenticate_cookai_user,
    edit_profile,
    get_my_profile,
    list_all_cookai_users,
    register_cookai_user,
)
from auth.schemas.auth_schema import UserRegister
from projects.cookAi.schemas.cookai_user_schema import CookAiUserUpdate


class TestRegisterCookaiUser:
    def test_creates_user_and_profile(self, session: Session):
        data = UserRegister(username="svcuser", email="svc@test.com", password="Pass123!")
        result = register_cookai_user(session, data)

        assert result.username == "svcuser"
        assert result.email == "svc@test.com"
        assert result.premium_member is False

    def test_creates_auth_provider(self, session: Session):
        data = UserRegister(username="svcprov", email="prov@test.com", password="Pass123!")
        register_cookai_user(session, data)

        # Verifica se AuthProvider foi criado
        user = session.exec(select(User).where(User.email == "prov@test.com")).first()
        providers = session.exec(select(AuthProvider).where(AuthProvider.user_id == user.id)).all()
        assert len(providers) == 1
        assert providers[0].provider == "local"


class TestAuthenticateCookaiUser:
    def test_returns_token(self, session: Session, sample_user_with_password):
        token = authenticate_cookai_user(session, "test@test.com", "Test1234!")
        assert isinstance(token, str)
        assert len(token) > 0

    def test_raises_401_wrong_password(self, session: Session, sample_user_with_password):
        with pytest.raises(HTTPException) as exc:
            authenticate_cookai_user(session, "test@test.com", "Wrong!")
        assert exc.value.status_code == 401

    def test_raises_401_unknown_email(self, session: Session):
        with pytest.raises(HTTPException) as exc:
            authenticate_cookai_user(session, "nobody@test.com", "Test1234!")
        assert exc.value.status_code == 401


class TestListAllCookaiUsers:
    def test_returns_empty_list(self, session: Session):
        result = list_all_cookai_users(session)
        assert result == []

    def test_returns_all_profiles(self, session: Session, sample_profile):
        result = list_all_cookai_users(session)
        assert len(result) == 1
        assert result[0].username == "testuser"


class TestGetMyProfile:
    def test_returns_existing_profile(self, session: Session, sample_profile, sample_user):
        result = get_my_profile(session, sample_user.id)
        assert result.username == "testuser"

    def test_creates_profile_if_not_exists(self, session: Session, sample_user):
        """get_my_profile auto-cria perfil para usuários OAuth."""
        result = get_my_profile(session, sample_user.id)
        assert result.user_id == sample_user.id


class TestEditProfile:
    def test_updates_bios(self, session: Session, sample_profile, sample_user):
        updates = CookAiUserUpdate(bios="Nova bio")
        result = edit_profile(session, sample_user.id, updates)
        assert result.bios == "Nova bio"

    def test_none_bios_keeps_old(self, session: Session, sample_profile, sample_user):
        edit_profile(session, sample_user.id, CookAiUserUpdate(bios="Original"))
        result = edit_profile(session, sample_user.id, CookAiUserUpdate(bios=None))
        assert result.bios == "Original"

    def test_raises_404_no_profile(self, session: Session):
        fake_id = uuid4()
        with pytest.raises(HTTPException) as exc:
            edit_profile(session, fake_id, CookAiUserUpdate(bios="x"))
        assert exc.value.status_code == 404
