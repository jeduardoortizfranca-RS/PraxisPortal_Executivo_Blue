# backend/core/__init__.py

"""
Praxis AI Core - Módulos centrais da aplicação.
"""

from .config import settings
from .supabase_client import supabase

__all__ = ["settings", "supabase"]
