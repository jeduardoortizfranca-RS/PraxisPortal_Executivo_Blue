"""
Modelos Pydantic para Usuários - Praxis AI Core
Gerencia entrada, saída e atualização de dados de usuários.
"""

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# --------------------------------------------------------------------------
# MODELOS BÁSICOS
# --------------------------------------------------------------------------

class UserBase(BaseModel):
    """Modelo base com campos comuns a todas as representações de usuário."""
    email: EmailStr


class UserLogin(UserBase):
    """Modelo usado para login de usuário."""
    password: str


class UserRegister(UserBase):
    """Modelo usado para registro de novo usuário."""
    password: str
    confirm_password: Optional[str] = None


# --------------------------------------------------------------------------
# MODELOS DE RESPOSTA E PERFIL
# --------------------------------------------------------------------------

class UserResponse(UserBase):
    """Modelo usado em respostas da API (retorno de dados de usuário)."""
    id: str
    role: str = "user"
    plan: str = "free"
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserProfile(UserResponse):
    """Perfil completo do usuário (visualização pública/privada)."""
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None


# --------------------------------------------------------------------------
# MODELO DE ATUALIZAÇÃO DE PERFIL
# --------------------------------------------------------------------------

class UserProfileUpdate(BaseModel):
    """
    Modelo para atualização (PUT/PATCH) do perfil do usuário.
    Todos os campos são opcionais, pois o usuário pode atualizar apenas alguns.
    """
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    # Se quiser permitir atualização de senha ou plano no futuro, adicione:
    # password: Optional[str] = None
    # plan: Optional[str] = None

