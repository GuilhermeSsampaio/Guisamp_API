import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from sqlmodel.pool import StaticPool

from main import app
from config.db import get_session
from config.models import setup_models

from auth.models.user import User
from auth.models.auth_provider import AuthProvider
from auth.security.hashing import hash_password
from auth.security.tokens import create_access_token

from projects.cookAi.models.cookai_user import CookAiUser
from projects.cookAi.models.recipe import Recipe


@pytest.fixture(name="engine")
def engine_fixture():
    """Engine SQLite em memória — recriado por teste."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    setup_models()
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="session")
def session_fixture(engine):
    """Sessão isolada por teste."""
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session):
    """TestClient com session sobrescrita."""

    def get_session_override():
        yield session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


# ── Factories ────────────────────────────────────────────────


@pytest.fixture(name="sample_user")
def sample_user_fixture(session):
    """Cria um User base no banco."""
    user = User(username="testuser", email="test@test.com")
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture(name="sample_user_with_password")
def sample_user_with_password_fixture(session, sample_user):
    """Cria User + AuthProvider com senha 'Test1234!'."""
    provider = AuthProvider(
        user_id=sample_user.id,
        provider="local",
        password_hash=hash_password("Test1234!"),
    )
    session.add(provider)
    session.commit()
    return sample_user


@pytest.fixture(name="auth_token")
def auth_token_fixture(sample_user_with_password):
    """Gera um JWT válido para o sample_user."""
    return create_access_token({"sub": str(sample_user_with_password.id)})


@pytest.fixture(name="auth_headers")
def auth_headers_fixture(auth_token):
    """Headers com Bearer token."""
    return {"Authorization": f"Bearer {auth_token}"}


@pytest.fixture(name="sample_profile")
def sample_profile_fixture(session, sample_user_with_password):
    """Cria um CookAiUser (perfil) vinculado ao sample_user."""
    profile = CookAiUser(
        user_id=sample_user_with_password.id,
        premium_member=False,
    )
    session.add(profile)
    session.commit()
    session.refresh(profile)
    return profile


@pytest.fixture(name="sample_recipe")
def sample_recipe_fixture(session, sample_profile):
    """Cria uma receita vinculada ao sample_profile."""
    recipe = Recipe(
        title="Bolo de Cenoura",
        content="## Ingredientes\n- 3 cenouras",
        font="https://exemplo.com",
        link="https://exemplo.com/bolo",
        cookai_user_id=sample_profile.id,
    )
    session.add(recipe)
    session.commit()
    session.refresh(recipe)
    return recipe


# ── Segundo usuário (para testar permissões) ────────────────


@pytest.fixture(name="other_user")
def other_user_fixture(session):
    """Cria um segundo User."""
    user = User(username="otheruser", email="other@test.com")
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture(name="other_profile")
def other_profile_fixture(session, other_user):
    """Cria perfil CookAi para o segundo usuário."""
    provider = AuthProvider(
        user_id=other_user.id,
        provider="local",
        password_hash=hash_password("Other1234!"),
    )
    session.add(provider)
    session.commit()

    profile = CookAiUser(user_id=other_user.id, premium_member=False)
    session.add(profile)
    session.commit()
    session.refresh(profile)
    return profile


@pytest.fixture(name="other_auth_headers")
def other_auth_headers_fixture(other_user):
    """Headers com Bearer token do segundo usuário."""
    token = create_access_token({"sub": str(other_user.id)})
    return {"Authorization": f"Bearer {token}"}
