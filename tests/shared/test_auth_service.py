"""Testes para auth/services — auth_service e oauth_service."""
from uuid import uuid4
from sqlmodel import Session, select

from auth.models.user import User
from auth.models.auth_provider import AuthProvider
from auth.security.hashing import hash_password
from auth.services.auth_service import (
    authenticate_user,
    create_user,
    login_user,
)
from auth.services.oauth_service import get_or_create_oauth_user
from auth.schemas.auth_schema import UserRegister


class TestCreateUser:
    def test_creates_user_and_provider(self, session: Session):
        data = UserRegister(username="authuser", email="auth@test.com", password="Pass123!")
        user = create_user(session, data)

        assert user.username == "authuser"
        assert user.email == "auth@test.com"
        assert user.id is not None


class TestAuthenticateUser:
    def test_valid_credentials(self, session: Session, sample_user_with_password):
        user = authenticate_user(session, "test@test.com", "Test1234!")
        assert user is not None
        assert user.email == "test@test.com"

    def test_wrong_password(self, session: Session, sample_user_with_password):
        result = authenticate_user(session, "test@test.com", "Wrong!")
        assert result is None

    def test_unknown_email(self, session: Session):
        result = authenticate_user(session, "nobody@test.com", "Pass!")
        assert result is None


class TestLoginUser:
    def test_returns_token(self, session: Session, sample_user_with_password):
        token = login_user(session, "test@test.com", "Test1234!")
        assert isinstance(token, str)
        assert len(token) > 0

    def test_returns_none_invalid(self, session: Session, sample_user_with_password):
        result = login_user(session, "test@test.com", "Wrong!")
        assert result is None


class TestGetOrCreateOauthUser:
    def test_creates_new_user(self, session: Session):
        user = get_or_create_oauth_user(session, "google@test.com", "google", "sub-123")
        assert user.email == "google@test.com"

    def test_returns_existing_user(self, session: Session, sample_user):
        user = get_or_create_oauth_user(session, "test@test.com", "google", "sub-456")
        assert user.id == sample_user.id

    def test_links_provider_if_missing(self, session: Session, sample_user):
        """Se user existe mas não tem provider google, vincula."""
        get_or_create_oauth_user(session, "test@test.com", "google", "sub-789")

        providers = session.exec(
            select(AuthProvider).where(
                AuthProvider.user_id == sample_user.id,
                AuthProvider.provider == "google",
            )
        ).all()
        assert len(providers) == 1

    def test_does_not_duplicate_provider(self, session: Session):
        """Chamar 2x não cria provider duplicado."""
        get_or_create_oauth_user(session, "dup@test.com", "google", "sub-1")
        get_or_create_oauth_user(session, "dup@test.com", "google", "sub-1")

        user = session.exec(select(User).where(User.email == "dup@test.com")).first()
        providers = session.exec(
            select(AuthProvider).where(
                AuthProvider.user_id == user.id,
                AuthProvider.provider == "google",
            )
        ).all()
        assert len(providers) == 1
