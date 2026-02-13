from fastapi import APIRouter, HTTPException, Request
from config.db import SessionDep
from config.settings import  GOOGLE_REDIRECT_URI
from auth.services.oauth_service import get_or_create_oauth_user
from auth.security.tokens import create_access_token
from auth.schemas.token_schema import TokenResponse
from auth.security.google_setup import oauth

# Define o prefixo. As URLs finais serão /auth/google e /auth/google/callback
router = APIRouter(prefix="/auth/google", tags=["OAuth"])

@router.get("/")
async def google_login(request: Request):
    """Redireciona o usuário para a página de login do Google"""
    
    # Debug: Verifica no terminal o que está sendo usado
    print(f"Tentando login Google com Redirect URI: '{GOOGLE_REDIRECT_URI}'")

    if not GOOGLE_REDIRECT_URI:
        raise HTTPException(status_code=500, detail="Configuração de REDIRECT_URI está vazia.")

    # Passamos explicitamente o redirect_uri aqui
    return await oauth.google.authorize_redirect(request, GOOGLE_REDIRECT_URI)

@router.get("/callback", response_model=TokenResponse)
async def google_callback(request: Request, session: SessionDep):
    """Recebe o retorno do Google, cria o usuário se necessário e gera token JWT"""
    try:
        token = await oauth.google.authorize_access_token(request)
    except Exception as e:
        # Captura erro caso o usuário cancele ou o token seja inválido
        raise HTTPException(status_code=400, detail=f"Erro na autenticação: {str(e)}")

    user_info = token.get("userinfo")
    if not user_info:
        raise HTTPException(status_code=400, detail="Não foi possível obter dados do Google")

    email = user_info.get("email")
    provider_sub = user_info.get("sub") # ID único do usuário no Google

    if not email:
        raise HTTPException(status_code=400, detail="Email não retornado pelo Google")

    # Lógica de negócio via Service
    user = get_or_create_oauth_user(session, email, "google", provider_sub)

    # Gera o token da API (interno)
    access_token = create_access_token(data={"sub": str(user.id)})
    
    return {"access_token": access_token, "token_type": "bearer"}