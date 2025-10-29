from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(
    title="PraxisPortal API",
    version="1.0.0",
)

@app.get("/")
async def root():
    return JSONResponse(
        content={"status": "✅ API FastAPI ativa na Vercel"}
    )
