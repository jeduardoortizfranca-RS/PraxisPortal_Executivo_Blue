# backend/core/supabase_client.py
"""
Cliente Supabase Centralizado - Solução para importações circulares
Versão: 1.0.0 - Estável
"""
import os
from dotenv import load_dotenv
from supabase import create_client, Client
from typing import Optional

# Carrega variáveis de ambiente
load_dotenv()

# Configuração Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Validação crítica das credenciais
if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError(
        "❌ ERRO CRÍTICO: SUPABASE_URL e/ou SUPABASE_KEY não encontrados no .env\n"
        "Verifique o arquivo .env na raiz do projeto."
    )

# Cliente Supabase global (singleton)
supabase_client: Optional[Client] = None

def get_supabase_client() -> Client:
    """
    Retorna o cliente Supabase inicializado.
    Garante que só seja criado uma vez.
    """
    global supabase_client

    if supabase_client is None:
        try:
            supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
            print("✅ Supabase Client inicializado com sucesso (v2.24.0)")

            # Teste de conectividade básico
            test_response = supabase_client.from_('transacoes').select('id').limit(1).execute()
            print(f"   📡 Conexão Supabase: OK (resposta: {len(test_response.data)} registros)")

        except Exception as e:
            print(f"❌ Erro ao inicializar Supabase: {str(e)}")
            raise RuntimeError(f"Falha na conexão Supabase: {str(e)}")

    return supabase_client

# Exporta o cliente para uso direto (se necessário)
supabase = get_supabase_client()
