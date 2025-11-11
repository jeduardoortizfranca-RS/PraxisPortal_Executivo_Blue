# backend/routes/rotas_leads.py
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from supabase import Client

from backend.dependencies import get_supabase_client

router = APIRouter()

# Exemplo de modelo Pydantic para Leads (ajuste conforme necessário)
class Lead(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100)
    email: str = Field(..., pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    telefone: Optional[str] = None
    origem: Optional[str] = None
    data_criacao: datetime = Field(default_factory=datetime.now)
    status: str = Field("novo", pattern="^(novo|contatado|qualificado|desqualificado|convertido)$")

class LeadOut(Lead):
    id: int
    created_at: datetime

TBL_LEADS = "leads" # Nome da tabela de leads no Supabase

@router.get("/health-leads")
async def health_leads(
    supabase: Client = Depends(get_supabase_client)
):
    """Endpoint de teste para rotas de leads."""
    try:
        # Tenta fazer uma consulta simples para verificar a conexão com o Supabase
        supabase.table(TBL_LEADS).select("id").limit(1).execute()
        supabase_connected = True
    except Exception:
        supabase_connected = False

    return {
        "status": "leads_ok",
        "supabase_connected": supabase_connected,
        "message": "Rotas de leads funcionando!"
    }

@router.post("/criar", response_model=LeadOut, status_code=status.HTTP_201_CREATED)
async def criar_lead(
    lead: Lead,
    supabase: Client = Depends(get_supabase_client)
):
    """Cria um novo lead no Supabase."""
    try:
        response = supabase.table(TBL_LEADS).insert(lead.model_dump()).execute()
        if response.data:
            return response.data[0]
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao criar lead.")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro inesperado: {str(e)}")

# Adicione outras rotas de leads aqui (GET, PUT, DELETE) conforme necessário
