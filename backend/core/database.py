"""
Centraliza configuração de banco de dados (Supabase + SQLAlchemy)
Este arquivo NÃO importa nada do resto do projeto
"""
import os
from dotenv import load_dotenv
from supabase import create_client, Client
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Carrega variáveis de ambiente ANTES de qualquer coisa
load_dotenv()

# -----------------------------
# CONFIGURAÇÃO SUPABASE
# -----------------------------
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError(
        "❌ ERRO CRÍTICO: SUPABASE_URL e/ou SUPABASE_KEY não encontrados no .env"
    )

# Instância global única do Supabase
supabase_client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# -----------------------------
# CONFIGURAÇÃO SQLALCHEMY (SQLite local)
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "praxis_local.db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Dependência para sessões SQLAlchemy"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

print("✅ Database module carregado com sucesso")
print(f"   📡 Supabase: {SUPABASE_URL[:20]}...")
print(f"   💾 SQLite: {DB_PATH}")
