from typing import List
from fastapi import Depends, FastAPI, APIRouter, HTTPException,status
from sqlmodel import select
from uuid import UUID

from auth.models.auth_provider import AuthProvider
from auth.models.user import User
from auth.schemas.auth_schema import UserLogin, UserRegister
from auth.schemas.token_schema import TokenResponse
from auth.security.dependencies import current_user
from auth.security.hashing import hash_password
from auth.services.auth_service import login_user
from config.db import SessionDep
from sqlalchemy.orm import joinedload 

from projects.cookAi.models.cookai_user import CookAiUser
from projects.cookAi.schemas.cookai_user_schema import CookAiUserResponse, CookAiUserUpdate

router = APIRouter()

@router.post("/register", response_model=CookAiUserResponse)
def cookai_user_register(user_data: UserRegister, session: SessionDep):
    
    user_base = User(
        username=user_data.username,
        email=user_data.email,
    )

    session.add(user_base)
    session.commit()
    session.refresh(user_base)

    auth_provider = AuthProvider(
        user_id=user_base.id,
        provider="local",
        password_hash=hash_password(user_data.password)
    )

    session.add(auth_provider)
    session.commit()

    cookai_user = CookAiUser(
        user_id=user_base.id,
        premium_member=False
    )
    session.add(cookai_user)
    session.commit()
    session.refresh(cookai_user)

    return CookAiUserResponse(
        id =cookai_user.id,
        username= user_base.username,
        email=user_base.email,
        user_id=user_base.id,
        bios=cookai_user.bios,
        premium_member=cookai_user.premium_member
    )
    

@router.post("/login", response_model=TokenResponse)
def cookai_login(login_data:UserLogin, session: SessionDep):
    """
    Realiza login reutilizando o núcleo de autenticação.
    Retorna o Token JWT padrão.
    """
    token = login_user(session, login_data.email, login_data.password)

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas"
        )
    
    return {"access_token":token, "token_type": "bearer"}

@router.get("/list_cookai_users", response_model=List[CookAiUserResponse])
def list_cookai_users(session: SessionDep):
    # faz uma única consulta e traz todos
    cookai_profiles = session.exec(select(CookAiUser).options(
        joinedload(CookAiUser.user)
    )).all()

    results = []

    for profile in cookai_profiles:
        results.append(CookAiUserResponse(
            id=profile.id,
            user_id=profile.user.id,
            username=profile.user.username,
            email=profile.user.email,
            bios=profile.bios,
            premium_member=profile.premium_member
        ))
    
    return results


@router.put("/edit_profile", response_model=CookAiUserResponse)
def update_profile(
    updates: CookAiUserUpdate,
    session: SessionDep,
    user_id: str = Depends(current_user)
):
    # 1. Converta o ID de string para UUID
    user_uuid = UUID(user_id) 

    # 2. Use o UUID na busca
    statement = select(CookAiUser).where(CookAiUser.user_id == user_uuid)
    cookai_profile = session.exec(statement).first()

    if not cookai_profile:
        raise HTTPException(status_code=404, detail="Perfil CookAi não encontrado")
    
    if updates.bios is not None:
        cookai_profile.bios = updates.bios
    
    session.add(cookai_profile)
    session.commit()
    session.refresh(cookai_profile)

    return CookAiUserResponse(
        id=cookai_profile.id,
        user_id=cookai_profile.user_id,
        username=cookai_profile.user.username,
        email=cookai_profile.user.email,
        bios=cookai_profile.bios,
        premium_member=cookai_profile.premium_member
    )

@router.post("/save_Recipe")
def save_recipe():
    pass

@router.get("my_recipes")
def get_my_recipes():
    pass

@router.put("/update_recipe/{recipe_id}")
def update_recipe():
    pass

@router.delete("/delete_recipe/{recipe_id}")
def delete_recipe():
    pass