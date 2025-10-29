from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ----------------------------
# IMPORTAÇÕES DO BACKEND
# ----------------------------
from backend.database import Base, engine
from backend.routes import rotas_base, rotas_financeiro

# ----------------------------
# APP
# ----------------------------
app = FastAPI(
    title="PraxisPortal API",
    version="1.0.0",
    description="Backend FastAPI hospedado na Vercel",
)

# ----------------------------
# DB
# ----------------------------
Base.metadata.create_all(bind=engine)

# ----------------------------
# CORS
# ----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# ROTAS
# ----------------------------
app.include_router(rotas_base.router)
app.include_router(rotas_financeiro.router)

# ----------------------------
# ROTA RAIZ
# ----------------------------
@app.get("/")
async def root():
    return {"status": "✅ OK", "msg": "PraxisPortal API funcionando"}
