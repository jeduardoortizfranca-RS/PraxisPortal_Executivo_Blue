from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
def root():
    return JSONResponse({"status": "online", "message": "PraxisPortal API ativa e funcionando!"})
