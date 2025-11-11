# backend/routes/rotas_usuarios.py
from fastapi import APIRouter, HTTPException
from typing import Optional, Literal
from pydantic import BaseModel
from datetime import datetime
from backend.core.supabase_client import get_supabase_client

router = APIRouter()

class UsuarioCreate(BaseModel):
    id: str # User ID do Supabase Auth
    email: str
    nome: Optional[str] = None
    tipo_usuario: Literal["lead", "trial", "cliente_pago", "parceiro"] = "lead"
    status_mkt: str = "novo_cadastro"
    primeiro_servico: Optional[str] = None
    valor_total_gasto: float = 0.00

class UsuarioResponse(UsuarioCreate):
    data_cadastro: str
    ultima_atividade: str

@router.post("/usuarios", response_model=UsuarioResponse, status_code=201)
async def create_or_update_usuario(usuario_data: UsuarioCreate):
    client = get_supabase_client()

    # Tenta buscar o usuário
    existing_user = client.table('usuarios').select('*').eq('id', usuario_data.id).execute()

    if existing_user.data:
        # Atualiza usuário existente
        update_data = usuario_data.model_dump(exclude_unset=True)
        update_data['ultima_atividade'] = datetime.now().isoformat()
        response = client.table('usuarios').update(update_data).eq('id', usuario_data.id).execute()
        if response.data: # Adicionado esta verificação
            return response.data[0]
        else:
            raise HTTPException(status_code=500, detail="Erro ao atualizar usuário no Supabase.")
    else:
        # Cria novo usuário
        insert_data = usuario_data.model_dump(exclude_unset=True)
        response = client.table('usuarios').insert(insert_data).execute()
        if response.data: # Adicionado esta verificação
            return response.data[0]
        else:
            raise HTTPException(status_code=500, detail="Erro ao criar usuário no Supabase.")

@router.get("/usuarios/{user_id}", response_model=UsuarioResponse)
async def get_usuario(user_id: str):
    client = get_supabase_client()
    response = client.table('usuarios').select('*').eq('id', user_id).execute()
    if response.data:
        return response.data[0]
    raise HTTPException(status_code=404, detail="Usuário não encontrado")

# Esta linha de print deve estar no nível superior, sem indentação extra
print("👤 Módulo de Usuários carregado com sucesso!")
