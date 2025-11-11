"""
Configurações da Aplicação Praxis AI Core
Gerencia variáveis de ambiente e configurações globais
"""
from dotenv import load_dotenv # <--- ADICIONE ESTA LINHA
load_dotenv() # <--- ADICIONE ESTA LINHA

import os
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict # Importação corrigida

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )
    # App Settings
    PROJECT_NAME: str = Field(default="Praxis AI Core", description="Nome do projeto")
    VERSION: str = Field(default="1.0.0", description="Versão da aplicação")
    DEBUG: bool = Field(default=False, description="Modo debug (True/False)")
    # Supabase Settings
    SUPABASE_URL: str = Field(..., description="URL do projeto Supabase")
    SUPABASE_KEY: str = Field(..., description="Chave de serviço (anon key) do Supabase")
    # Stripe Settings
    STRIPE_SECRET_KEY: Optional[str] = Field(default=None, description="Chave secreta da API Stripe")
    STRIPE_PUBLIC_KEY: Optional[str] = Field(default=None, description="Chave pública da API Stripe")
    STRIPE_WEBHOOK_SECRET: Optional[str] = Field(default=None, description="Chave secreta do webhook Stripe")
    # Security Settings
    SECRET_KEY: str = Field(..., description="Chave secreta para JWT e outras operações de segurança")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    # Database Settings (Opcional, para fallback local)
    DATABASE_URL: Optional[str] = Field(default=None, description="URL do banco de dados")
    # Email Settings (Opcional)
    EMAIL_HOST: Optional[str] = Field(default=None, description="Servidor SMTP")
    EMAIL_PORT: Optional[int] = Field(default=None, description="Porta SMTP")
    EMAIL_USER: Optional[str] = Field(default=None, description="Usuário email")
    EMAIL_PASSWORD: Optional[str] = Field(default=None, description="Senha email")
    EMAIL_FROM: Optional[str] = Field(default=None, description="Email remetente")
# Instância global das configurações
settings = Settings()
# Função para validar configurações obrigatórias
def validate_required_settings():
    """
    Valida se as configurações obrigatórias estão definidas.
    """
    required = [
        "SUPABASE_URL",
        "SUPABASE_KEY",
        "SECRET_KEY"
    ]
    missing = []
    for key in required:
        if not getattr(settings, key, None):
            missing.append(key)
    if missing:
        raise ValueError(f"Configurações obrigatórias ausentes: {', '.join(missing)}")
    print(f"✅ Configurações validadas: {len(required)}/ {len(required)} OK")
    return True
if __name__ == "__main__":
    # Teste das configurações (opcional)
    try:
        validate_required_settings()
        print("Configurações carregadas com sucesso!")
    except Exception as e:
        print(f"Erro nas configurações: {e}")
