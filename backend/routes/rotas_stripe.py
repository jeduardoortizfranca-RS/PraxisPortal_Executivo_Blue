# backend/routes/rotas_stripe.py
from fastapi import APIRouter, Depends
from supabase import Client
from backend.dependencies import get_supabase_client

router = APIRouter()

@router.get("/health-stripe")
async def health_stripe(
    supabase: Client = Depends(get_supabase_client)
):
    """Endpoint de teste para rotas do Stripe."""
    return {
        "status": "stripe_ok",
        "supabase_connected": True, # Assumimos que get_supabase_client já validou
        "message": "Rotas do Stripe funcionando!"
    }

# Adicione suas rotas do Stripe aqui
