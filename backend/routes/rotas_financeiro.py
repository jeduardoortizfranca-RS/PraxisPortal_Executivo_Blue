# backend/routes/rotas_financeiro.py
"""
Rotas Financeiras - Módulo Principal
Endpoints para transações, relatórios e dashboards
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional, Dict
from pydantic import BaseModel
from datetime import datetime, date
from backend.core.supabase_client import get_supabase_client

router = APIRouter()

class TransacaoCreate(BaseModel):
    """Modelo para criar transação"""
    valor: float
    descricao: str
    categoria: str
    # Alterado de 'data: date' para 'created_at: datetime' para corresponder ao Supabase
    created_at: datetime = datetime.now() 
    tipo: str = "receita"  # receita ou despesa

class TransacaoResponse(BaseModel):
    """Modelo para resposta de transação"""
    id: Optional[int] = None
    valor: float
    descricao: str
    categoria: str
    # Alterado de 'data: str' para 'created_at: str' (Supabase retorna como string)
    created_at: str 
    tipo: str

# ----------------------------------------------------------------------
# ENDPOINT: LISTAR TRANSAÇÕES
# ----------------------------------------------------------------------
@router.get("/transacoes", response_model=List[TransacaoResponse])
async def get_transacoes(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    categoria: Optional[str] = None, # Adicionado filtro por categoria
    start_date: Optional[str] = None, # Formato YYYY-MM-DD
    end_date: Optional[str] = None # Formato YYYY-MM-DD
):
    """
    Lista transações financeiras com opções de filtro e paginação.
    Query params: limit, offset, categoria, start_date (YYYY-MM-DD), end_date (YYYY-MM-DD)
    """
    try:
        client = get_supabase_client() # Instancia o cliente dentro da função

        # Query base
        query = client.table('transacoes').select(
            'id, valor, descricao, categoria, created_at, tipo' # Alterado 'data' para 'created_at'
        )

        # Filtros
        if categoria:
            query = query.eq("categoria", categoria)
        if start_date:
            # Supabase timestamptz precisa de formato ISO, então adicionamos hora e fuso
            query = query.gte('created_at', f"{start_date}T00:00:00+00:00") # Alterado 'data' para 'created_at'
        if end_date:
            query = query.lte('created_at', f"{end_date}T23:59:59+00:00") # Alterado 'data' para 'created_at'

        # Ordenação
        query = query.order('created_at', desc=True) # Alterado 'data' para 'created_at'

        # Paginação
        response = query.range(offset, offset + limit - 1).execute()

        if response.data:
            return response.data
        else:
            return []
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar transações: {str(e)}")

# ----------------------------------------------------------------------
# ENDPOINT: RESUMO FINANCEIRO
# ----------------------------------------------------------------------
@router.get("/transacoes/resumo")
async def get_resumo_financeiro(
    start_date: Optional[str] = None, # Formato YYYY-MM-DD
    end_date: Optional[str] = None # Formato YYYY-MM-DD
):
    """
    Resumo financeiro: total receitas, despesas, saldo.
    Query params: start_date (YYYY-MM-DD), end_date (YYYY-MM-DD)
    """
    try:
        client = get_supabase_client() # Instancia o cliente dentro da função

        # Query para receitas
        receitas_query = client.table('transacoes').select(
            'valor'
        ).eq('tipo', 'receita')

        # Query para despesas
        despesas_query = client.table('transacoes').select(
            'valor'
        ).eq('tipo', 'despesa')

        # Aplicar filtros de data
        if start_date:
            receitas_query = receitas_query.gte('created_at', f"{start_date}T00:00:00+00:00") # Alterado 'data' para 'created_at'
            despesas_query = despesas_query.gte('created_at', f"{start_date}T00:00:00+00:00") # Alterado 'data' para 'created_at'
        if end_date:
            receitas_query = receitas_query.lte('created_at', f"{end_date}T23:59:59+00:00") # Alterado 'data' para 'created_at'
            despesas_query = despesas_query.lte('created_at', f"{end_date}T23:59:59+00:00") # Alterado 'data' para 'created_at'

        receitas = receitas_query.execute()
        despesas = despesas_query.execute()

        total_receitas = sum(item['valor'] for item in receitas.data)
        total_despesas = sum(item['valor'] for item in despesas.data)
        saldo = total_receitas - total_despesas

        return {
            "periodo": {
                "inicio": start_date or "indefinido",
                "fim": end_date or "indefinido"
            },
            "total_receitas": round(total_receitas, 2),
            "total_despesas": round(total_despesas, 2),
            "saldo": round(saldo, 2),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no resumo financeiro: {str(e)}")

# ----------------------------------------------------------------------
# ENDPOINT DE TESTE DO MÓDULO FINANCEIRO
# ----------------------------------------------------------------------
@router.get("/test")
async def test_financeiro_module(): # Renomeado para evitar conflito com o print final
    """
    Endpoint de teste para verificar a operacionalidade do módulo financeiro
    e a conectividade com o Supabase.
    """
    supabase_connected = False
    tabelas_acessiveis = []
    registros_estimados = 0
    try:
        client = get_supabase_client()
        # Tenta listar tabelas e fazer uma consulta simples
        # Nota: O método rpc('pg_tables') pode não estar disponível em todas as configurações.
        # Uma forma mais robusta de verificar a tabela 'transacoes' é tentar uma consulta nela.

        # Verifica se a tabela 'transacoes' existe e tem dados
        try:
            # Tenta selecionar um registro para verificar a existência da tabela
            response = client.table("transacoes").select("id").limit(1).execute()
            if response.data is not None: # Se não houver erro e data não for None, a tabela existe
                tabelas_acessiveis.append('transacoes')
                count_response = client.table("transacoes").select("count").execute()
                registros_estimados = count_response.data[0]['count'] if count_response.data else 0
            supabase_connected = True
        except Exception as table_check_e:
            # Se a tabela não existir ou houver outro erro, supabase_connected permanece False
            print(f"Aviso: Tabela 'transacoes' pode não existir ou erro ao acessá-la: {table_check_e}")
            supabase_connected = False # Garante que o status seja false se a tabela não for acessível

    except Exception as e:
        # Erro geral de conexão com Supabase
        raise HTTPException(status_code=500, detail=f"Erro de conexão ou consulta ao Supabase: {str(e)}")

    return {
        "status": "financeiro_ok",
        "supabase_connected": supabase_connected,
        "tabelas_acessiveis": tabelas_acessiveis,
        "registros_estimados": registros_estimados,
        "message": "Módulo financeiro operacional! 🎉",
        "endpoints_disponiveis": [
            "/financeiro/transacoes",
            "/financeiro/transacoes/resumo",
            "/financeiro/test",
            "/financeiro/transacoes?limit=5"
        ]
    }

print("💰 Módulo Financeiro carregado com sucesso!")
print("   📊 Endpoints: /financeiro/transacoes, /financeiro/resumo, /financeiro/test")
