from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from config.db import get_session
from auth.schemas.auth_schema import UserRegister, UserLogin
from auth.schemas.user_schema import UserResponse
from auth.schemas.token_schema import TokenResponse
from auth.services.auth_service import create_user, login_user
from auth.security.dependencies import current_user

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserResponse)
def register(user_data: UserRegister, session: Session = Depends(get_session)):
    try:
        user = create_user(session, user_data)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
@router.post("/login", response_model=TokenResponse)
def login(credentials: UserLogin, session: Session = Depends(get_session)):
    token = login_user(
        session, credentials.email, credentials.password
    )

    if not token:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas"
        )
    
    return {"access_token": token, "token_type": "bearer"}

@router.get("/protected")
def protected_route(user_id:str = Depends(current_user)):
    return {
        "message": "rota protegida acessada",
        "userid": user_id
    }