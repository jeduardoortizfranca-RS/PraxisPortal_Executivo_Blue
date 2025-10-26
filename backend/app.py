
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .models import *  # noqa
from .routes import rotas_base, rotas_financeiro

app = FastAPI(
    title="Núcleo de IA Praxis — API Local",
    description="API local com módulo financeiro e banco SQLite",
    version="0.1.0",
)

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rotas_base.router)
app.include_router(rotas_financeiro.router)

@app.get("/")
def raiz():
    return {"status": "ok", "mensagem": "Núcleo de IA Praxis — API Local ativa"}

def main():
    import uvicorn
    print("🚀 Iniciando Núcleo de IA Praxis — API Local em http://127.0.0.1:8000 ...")
    uvicorn.run("backend.app:app", host="127.0.0.1", port=8000, reload=False)

if __name__ == "__main__":
    main()
