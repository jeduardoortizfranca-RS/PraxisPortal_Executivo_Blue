# backend/dependencies.py
"""
Injeção de Dependências - Versão Limpa
Elimina importações circulares e centraliza o cliente Supabase
"""
from typing import Generator
from fastapi import Depends
from backend.core.supabase_client import get_supabase_client, supabase
from sqlalchemy.orm import Session

# Dependência para Supabase Client
def get_supabase() -> get_supabase_client:
    """
    Dependência FastAPI para injetar o cliente Supabase.
    """
    return get_supabase_client()

# Dependência para sessão SQLite (se necessário no futuro)
def get_db() -> Generator:
    """
    Dependência para sessão SQLite (placeholder para migração futura).
    """
    # Implementação SQLite será adicionada após estabilizar Supabase
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Cliente global para uso direto (evita Depends em alguns casos)
supabase_client = supabase
