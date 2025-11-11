from fastapi import FastAPI
from fastapi.responses import JSONResponse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PraxisPortal")

app = FastAPI(
    title="PraxisPortal API",
    version="1.0.0",
    description="Backend FastAPI estável para o projeto PraxisPortal Executivo Blue"
)

@app.get("/", summary="Rota principal", tags=["Status"])
async def root():
    logger.info("Rota raiz acessada.")
    return JSONResponse(content={
        "status": "online",
        "message": "PraxisPortal API rodando na Vercel 🚀"
    })

@app.get("/health", summary="Verificação de saúde", tags=["Status"])
async def health_check():
    logger.info("Health check executado.")
    return {"health": "ok", "environment": "production"}

@app.get("/info", summary="Informações da API", tags=["Informações"])
async def info():
    return {
        "project": "PraxisPortal Executivo Blue",
        "framework": "FastAPI",
        "runtime": "Python 3.12",
        "status": "running"
    }
