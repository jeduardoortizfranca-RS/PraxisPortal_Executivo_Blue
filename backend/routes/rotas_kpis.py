# backend/routes/rotas_kpis.py
from fastapi import APIRouter, Depends
from supabase import Client
from backend.dependencies import get_supabase_client

router = APIRouter()

@router.get("/health-kpis")
async def health_kpis(
    supabase: Client = Depends(get_supabase_client)
):
    """Endpoint de teste para rotas de KPIs."""
    return {
        "status": "kpis_ok",
        "supabase_connected": True, # Assumimos que get_supabase_client já validou
        "message": "Rotas de KPIs funcionando!"
    }

# Adicione suas rotas de KPIs aqui
