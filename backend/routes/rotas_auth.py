"""
Rotas de Autenticação - Praxis AI Core
Integração com Supabase Auth para o Portal Praxis
"""

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional

from backend.core.supabase_client import supabase
from backend.models.user import UserLogin, UserRegister, UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer()

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

@router.post("/login", response_model=TokenResponse)
async def login_user(credentials: UserLogin):
    """
    Login para o Portal Praxis AI Core via Supabase Auth
    """
    try:
        # Autenticação via Supabase
        result = supabase_client.auth.sign_in_with_password({
            "email": credentials.email,
            "password": credentials.password
        })
        
        if not result.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciais inválidas",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Obter dados do usuário com metadados da Praxis AI Core
        user_metadata = result.user.user_metadata or {}
        user_data = {
            "id": result.user.id,
            "email": result.user.email,
            "role": user_metadata.get("role", "user"),
            "plan": user_metadata.get("plan", "free"),
            "created_at": result.user.created_at
        }
        
        return TokenResponse(
            access_token=result.session.access_token,
            user=UserResponse(**user_data)
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Erro de autenticação: {str(e)}"
        )

@router.post("/register", response_model=UserResponse)
async def register_user(user_data: UserRegister):
    """
    Registro de novo usuário para o Portal Praxis AI Core
    """
    try:
        # Verificar se usuário já existe
        existing_user = supabase_client.db("profiles").select("id").eq("email", user_data.email).execute()
        if existing_user.data:
            raise HTTPException(
                status_code=400,
                detail="Usuário já cadastrado na Praxis AI Core"
            )
        
        # Registrar no Supabase Auth com metadados da Praxis
        result = supabase_client.auth.sign_up({
            "email": user_data.email,
            "password": user_data.password,
            "options": {
                "data": {
                    "role": "user",
                    "plan": "free",
                    "company": None,
                    "verified": False
                }
            }
        })
        
        if not result.user:
            raise HTTPException(
                status_code=400,
                detail="Erro ao criar conta na Praxis AI Core"
            )
        
        # Criar perfil no banco de dados
        user_profile = {
            "id": result.user.id,
            "email": user_data.email,
            "role": "user",
            "plan": "free",
            "analyses_count": 0,
            "created_at": result.user.created_at,
            "last_login": None,
            "company_name": None,
            "company_size": None
        }
        
        supabase_client.db("profiles").insert(user_profile).execute()
        
        # Enviar email de boas-vindas (implementar webhook ou serviço)
        print(f"Novo usuário registrado: {user_data.email}")
        
        return UserResponse(**user_profile)
        
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Erro no registro: {str(e)}"
        )

@router.get("/me", response_model=UserResponse)
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Obter dados do usuário logado no Portal Praxis
    """
    token = credentials.credentials
    
    # Verificar token no Supabase
    if not supabase_client.verify_token(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Obter dados do usuário com estatísticas
    user_data = supabase_client.get_user(token)
    if not user_data:
        raise HTTPException(
            status_code=401,
            detail="Usuário não encontrado no sistema"
        )
    
    # Buscar estatísticas adicionais do perfil
    profile = supabase_client.db("profiles").select("analyses_count, company_name, last_login").eq("id", user_data["id"]).execute()
    
    if profile.data:
        user_data.update({
            "analyses_count": profile.data[0].get("analyses_count", 0),
            "company_name": profile.data[0].get("company_name"),
            "last_login": profile.data[0].get("last_login")
        })
    
    return UserResponse(**user_data)

@router.post("/logout")
async def logout_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Logout do usuário do Portal Praxis AI Core
    """
    try:
        token = credentials.credentials
        supabase_client.auth.sign_out(token)
        
        # Atualizar last_login no perfil
        user_id = supabase_client.get_user(token)["id"]
        supabase_client.db("profiles").update({"last_login": "now()"}).eq("id", user_id).execute()
        
        return {"message": "Logout realizado com sucesso da Praxis AI Core"}
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Erro no logout: {str(e)}"
        )

@router.get("/profile/stats")
async def get_user_stats(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Estatísticas do usuário para o dashboard
    """
    token = credentials.credentials
    
    if not supabase_client.verify_token(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id = supabase_client.get_user(token)["id"]
    
    # Contar análises realizadas
    analyses = supabase_client.db("analyses").select("count").eq("user_id", user_id).execute()
    analyses_count = analyses.count if analyses.data else 0
    
    # Contar leads gerados (se aplicável)
    leads = supabase_client.db("leads").select("count").eq("owner_id", user_id).execute()
    leads_count = leads.count if leads.data else 0
    
    # Plano atual
    profile = supabase_client.db("profiles").select("plan, subscription_status").eq("id", user_id).execute()
    plan_info = profile.data[0] if profile.data else {"plan": "free", "subscription_status": "active"}
    
    return {
        "analyses_count": analyses_count,
        "leads_count": leads_count,
        "plan": plan_info["plan"],
        "subscription_status": plan_info["subscription_status"],
        "last_analysis": None  # Implementar busca da última análise
    }
