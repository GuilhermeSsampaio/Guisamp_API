from typing import List, Optional
from uuid import UUID
from sqlmodel import select, Session
from sqlalchemy.orm import joinedload

from projects.cookAi.models.cookai_user import CookAiUser


def list_cookai_users(session: Session) -> List[CookAiUser]:
    return session.exec(
        select(CookAiUser).options(joinedload(CookAiUser.user))
    ).all()


def get_cookai_user_by_user_id(session: Session, user_uuid: UUID) -> Optional[CookAiUser]:
    """Busca perfil CookAi pelo user_id (da tabela User). Retorna None se não existir."""
    return session.exec(
        select(CookAiUser)
        .options(joinedload(CookAiUser.user))
        .where(CookAiUser.user_id == user_uuid)
    ).first()


def create_cookai_user(session: Session, user_uuid: UUID) -> CookAiUser:
    """Cria um novo perfil CookAi vinculado ao user_id."""
    profile = CookAiUser(user_id=user_uuid, premium_member=False)
    session.add(profile)
    session.commit()
    session.refresh(profile)
    # Recarrega com relationship
    return session.exec(
        select(CookAiUser)
        .options(joinedload(CookAiUser.user))
        .where(CookAiUser.id == profile.id)
    ).first()


def update_cookai_user(session: Session, profile: CookAiUser) -> CookAiUser:
    session.add(profile)
    session.commit()
    session.refresh(profile)
    return profile
