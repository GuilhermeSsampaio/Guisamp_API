from uuid import UUID
from fastapi import HTTPException, status
from sqlmodel import Session

from auth.models.auth_provider import AuthProvider
from auth.models.user import User
from auth.schemas.auth_schema import UserRegister
from auth.security.hashing import hash_password
from auth.services.auth_service import login_user

from projects.cookAi.helpers.profile_helpers import get_profile_or_404, to_cookai_response
from projects.cookAi.repository.cookai_users_crud import (
    create_cookai_user,
    get_cookai_user_by_user_id,
    list_cookai_users,
    update_cookai_user,
)
from projects.cookAi.schemas.cookai_user_schema import CookAiUserResponse, CookAiUserUpdate


def register_cookai_user(session: Session, user_data: UserRegister) -> CookAiUserResponse:
    """Cria User base + AuthProvider + CookAiUser."""
    user_base = User(username=user_data.username, email=user_data.email)
    session.add(user_base)
    session.commit()
    session.refresh(user_base)

    auth_provider = AuthProvider(
        user_id=user_base.id,
        provider="local",
        password_hash=hash_password(user_data.password),
    )
    session.add(auth_provider)
    session.commit()

    profile = create_cookai_user(session, user_base.id)
    return to_cookai_response(profile)


def authenticate_cookai_user(session: Session, email: str, password: str) -> str:
    """Autentica e retorna o access_token JWT ou lança 401."""
    token = login_user(session, email, password)

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
        )

    return token


def list_all_cookai_users(session: Session) -> list[CookAiUserResponse]:
    """Lista todos os perfis CookAi."""
    profiles = list_cookai_users(session)
    return [to_cookai_response(p) for p in profiles]


def get_my_profile(session: Session, user_uuid: UUID) -> CookAiUserResponse:
    """Busca perfil do usuário autenticado. Cria se não existir (OAuth)."""
    profile = get_cookai_user_by_user_id(session, user_uuid)

    if not profile:
        profile = create_cookai_user(session, user_uuid)

    return to_cookai_response(profile)


def edit_profile(session: Session, user_uuid: UUID, updates: CookAiUserUpdate) -> CookAiUserResponse:
    """Atualiza o perfil do usuário autenticado."""
    profile = get_profile_or_404(session, user_uuid)

    if updates.bios is not None:
        profile.bios = updates.bios

    profile = update_cookai_user(session, profile)
    return to_cookai_response(profile)
