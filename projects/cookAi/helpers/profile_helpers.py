from uuid import UUID
from fastapi import HTTPException
from sqlmodel import Session

from projects.cookAi.models.cookai_user import CookAiUser
from projects.cookAi.repository.cookai_users_crud import get_cookai_user_by_user_id
from projects.cookAi.schemas.cookai_user_schema import CookAiUserResponse


def get_profile_or_404(session: Session, user_uuid: UUID) -> CookAiUser:
    """Busca perfil CookAi pelo user_id ou lança 404."""
    profile = get_cookai_user_by_user_id(session, user_uuid)

    if not profile:
        raise HTTPException(status_code=404, detail="Perfil CookAi não encontrado")

    return profile


def to_cookai_response(profile: CookAiUser) -> CookAiUserResponse:
    """Converte um CookAiUser (com user carregado) em CookAiUserResponse."""
    return CookAiUserResponse(
        id=profile.id,
        user_id=profile.user_id,
        username=profile.user.username,
        email=profile.user.email,
        bios=profile.bios,
        premium_member=profile.premium_member,
    )
