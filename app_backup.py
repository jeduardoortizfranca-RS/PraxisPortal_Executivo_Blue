from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.database import Base, engine
from backend.models import *  # noqa
from backend.routes import rotas_base, rotas_financeiro

# ------------------------------------------------------------
# Configuração principal da API
# ------------------------------------------------------------
app = FastAPI(
    title="Núcleo de IA Praxis — API Local",
    description="API local com módulo financeiro e banco SQLite",
    version="0.1.1",
)

# ------------------------------------------------------------
# Banco de dados
# ------------------------------------------------------------
Base.metadata.create_all(bind=engine)

# ------------------------------------------------------------
# Configuração de CORS
# ------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------
# Rotas de Módulos
# ------------------------------------------------------------
app.include_router(rotas_base.router)
app.include_router(rotas_financeiro.router)

# ------------------------------------------------------------
# Rota raiz (para evitar erro 404 na Vercel)
# ------------------------------------------------------------
@app.get("/")
def raiz():
    return {
        "status": "✅ OK",
        "mensagem": "Núcleo de IA Praxis — API Local ativa e operante na Vercel"
    }

# ------------------------------------------------------------
# Execução local
# ------------------------------------------------------------
def main():
    import uvicorn
    print("🚀 Iniciando Núcleo de IA Praxis — API Local em http://127.0.0.1:8000 ...")
    uvicorn.run("backend.app:app", host="127.0.0.1", port=8000, reload=False)

if __name__ == "__main__":
    main()
