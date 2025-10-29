from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# importa banco/models/rotas
from backend.database import Base, engine
from backend.routes import rotas_base, rotas_financeiro

# ------------------------------------------------------------
# APP
# ------------------------------------------------------------
app = FastAPI(
    title="PraxisPortal API",
    version="1.0.0",
    description="Backend FastAPI hospedado na Vercel",
)

# ------------------------------------------------------------
# DB
# ------------------------------------------------------------
try:
    Base.metadata.create_all(bind=engine)
except:
    pass   # Em serverless pode falhar — ignoramos

# ------------------------------------------------------------
# CORS
# ------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------
# Rotas
# ------------------------------------------------------------
app.include_router(rotas_base.router)
app.include_router(rotas_financeiro.router)

# ------------------------------------------------------------
# Rota raiz
# ------------------------------------------------------------
@app.get("/")
async def root():
    return {
        "status": "✅ OK",
        "msg": "PraxisPortal API funcionando",
        "db": "SQLite local"
    }
