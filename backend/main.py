# backend/main.py
"""
Praxis AI Core - Backend Principal
Versão Estável: Supabase Centralizado + Rotas Financeiras + Chatbot/Leads
"""
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from backend.core.supabase_client import get_supabase_client
from backend.routes.rotas_financeiro import router as financeiro_router
from backend.routes import rotas_usuarios
# --- NOVAS IMPORTAÇÕES AQUI ---
from backend.routes.rotas_chatbot_leads import router as chatbot_leads_router
# --- FIM DAS NOVAS IMPORTAÇÕES ---

# ----------------------------------------------------------------------
# Carrega variáveis de ambiente (.env)
# ----------------------------------------------------------------------
load_dotenv()

# ----------------------------------------------------------------------
# Instância principal
# ----------------------------------------------------------------------
app = FastAPI(
    title="🚀 Praxis AI Core - Plataforma Executiva",
    description="Sistema integrado de gestão financeira, leads e KPIs",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ----------------------------------------------------------------------
# CORS - permite que o frontend acesse a API
# ----------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------------------------------------------
# Inclui as rotas dos módulos
# ----------------------------------------------------------------------
app.include_router(financeiro_router, prefix="/financeiro", tags=["Financeiro"])
app.include_router(rotas_usuarios.router, prefix="/usuarios", tags=["Usuários"])
# --- NOVA INCLUSÃO DE ROUTER AQUI ---
app.include_router(chatbot_leads_router, prefix="/api/v1", tags=["Chatbot e Leads Jurídicos"])
# --- FIM DA NOVA INCLUSÃO DE ROUTER ---

# ----------------------------------------------------------------------
# HEALTH CHECK
# ----------------------------------------------------------------------
@app.get("/health")
async def health_check():
    """Verifica conectividade com o Supabase"""
    supabase_status = "unknown"
    try:
        client = get_supabase_client()
        # teste de consulta simples
        client.table("transacoes").select("id").limit(1).execute()
        supabase_status = "connected"
    except Exception as e:
        supabase_status = f"error: {str(e)[:80]}"
    return {
        "status": "healthy",
        "service": "Praxis AI Core - Plataforma Executiva",
        "version": app.version,
        "supabase": supabase_status,
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "root": "/",
            "health": "/health",
            "financeiro_test": "/financeiro/test",
            "financeiro_transacoes": "/financeiro/transacoes",
            "chatbot_interacoes": "/api/v1/chatbot/interacoes", # Adicionado para visibilidade
            "leads_juridicos": "/api/v1/leads/juridicos",       # Adicionado para visibilidade
            "docs": "/docs",
        },
    }

# ----------------------------------------------------------------------
# ROOT
# ----------------------------------------------------------------------
@app.get("/")
async def root():
    """Página raiz com instruções básicas"""
    return {
        "message": "🚀 Praxis AI Core - Plataforma Executiva",
        "status": "Sistema operacional",
        "version": app.version,
        "next_steps": [
            "1. Acesse /health para verificar conectividade",
            "2. Teste /financeiro/test para o módulo financeiro",
            "3. Teste /financeiro/transacoes para dados financeiros",
            "4. Teste /api/v1/chatbot/interacoes (POST) para registrar interações",
            "5. Teste /api/v1/leads/juridicos (POST) para criar leads",
            "6. Acesse /docs para a documentação interativa da API",
            "7. Configure o frontend em http://localhost:3000",
        ],
        "timestamp": datetime.now().isoformat(),
    }

# ----------------------------------------------------------------------
# Execução Local
# ----------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    print("🚀 Iniciando Praxis AI Core ...")
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)
print("✅ Backend Praxis AI Core carregado com sucesso!")
print("   📡 Servidor: http://localhost:8001")
print("   🩺 Health:   http://localhost:8001/health")
print("   💰 Financeiro: http://localhost:8001/financeiro/transacoes")
print("   💬 Chatbot/Leads: http://localhost:8001/api/v1/chatbot/interacoes (POST)")
