from fastapi import FastAPI
from fastapi.responses import JSONResponse
import logging

# --- Configuração de logs ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PraxisPortal")

# --- Inicialização do app ---
app = FastAPI(
    title="PraxisPortal API",
    version="1.0.0",
    description="Backend FastAPI estável para o projeto PraxisPortal Executivo Blue"
)

# --- Rotas principais ---
@app.get("/", summary="Rota principal", tags=["Status"])
async def root():
    """
    Rota padrão que confirma se a API está ativa.
    """
    logger.info("Rota raiz acessada.")
    return JSONResponse(content={
        "status": "online",
        "message": "PraxisPortal API ativa e funcionando na Vercel 🚀"
    })

@app.get("/health", summary="Verificação de saúde", tags=["Status"])
async def health_check():
    """
    Rota de verificação de saúde (para monitoramento e deploys).
    """
    logger.info("Health check executado com sucesso.")
    return {"health": "ok", "environment": "production"}

@app.get("/info", summary="Informações da API", tags=["Informações"])
async def info():
    """
    Exibe informações básicas da API.
    """
    return {
        "project": "PraxisPortal Executivo Blue",
        "framework": "FastAPI",
        "runtime": "Python 3.12",
        "status": "running"
    }

# --- Tratamento global de exceções ---
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Erro inesperado: {exc}")
    return JSONResponse(status_code=500, content={"error": "Erro interno no servidor", "details": str(exc)})
