# backend/routes/rotas_chatbot_leads.py
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime
from backend.core.supabase_client import get_supabase_client
from backend.utils.email_service import send_email # Precisaremos criar este arquivo

router = APIRouter()

# --- Modelos Pydantic ---

class InteracaoChatbotBase(BaseModel):
    """Base para interações do chatbot."""
    usuario_id: Optional[str] = Field(None, description="ID do usuário que interagiu com o chatbot.")
    pergunta: str = Field(..., min_length=1, description="A pergunta feita pelo usuário ao chatbot.")
    resposta: str = Field(..., min_length=1, description="A resposta fornecida pelo chatbot.")
    topicos_identificados: Optional[List[str]] = Field(None, description="Tópicos ou palavras-chave identificados na interação.")
    satisfacao_usuario: Optional[int] = Field(None, ge=1, le=5, description="Nível de satisfação do usuário (1 a 5).")
    feedback_usuario: Optional[str] = Field(None, description="Feedback textual do usuário sobre a interação.")

class InteracaoChatbotCreate(InteracaoChatbotBase):
    """Modelo para criar uma nova interação do chatbot."""
    # created_at e updated_at serão gerados automaticamente pelo Supabase/backend
    pass

class InteracaoChatbotInDB(InteracaoChatbotBase):
    """Modelo para interações do chatbot como armazenadas no banco de dados."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class LeadJuridicoBase(BaseModel):
    """Base para leads jurídicos gerados pelo chatbot."""
    interacao_id: int = Field(..., description="ID da interação do chatbot que gerou o lead.")
    nome_completo: str = Field(..., min_length=3, description="Nome completo do potencial cliente.")
    email: EmailStr = Field(..., description="Endereço de e-mail do potencial cliente.")
    telefone: Optional[str] = Field(None, description="Número de telefone do potencial cliente.")
    tipo_caso: Optional[str] = Field(None, description="Tipo de caso jurídico (ex: divórcio, trabalhista, imobiliário).")
    descricao_problema: str = Field(..., min_length=10, description="Breve descrição do problema jurídico.")
    status_lead: str = Field("Novo", description="Status atual do lead (ex: Novo, Contatado, Qualificado, Perdido).")
    prioridade: str = Field("Média", description="Prioridade do lead (Baixa, Média, Alta).")
    observacoes: Optional[str] = Field(None, description="Observações adicionais sobre o lead.")

class LeadJuridicoCreate(LeadJuridicoBase):
    """Modelo para criar um novo lead jurídico."""
    # created_at e updated_at serão gerados automaticamente pelo Supabase/backend
    pass

class LeadJuridicoInDB(LeadJuridicoBase):
    """Modelo para leads jurídicos como armazenados no banco de dados."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# --- Funções de Conexão com Supabase ---

def get_db():
    """Retorna uma instância do cliente Supabase."""
    return get_supabase_client()

# --- Endpoints de Interações do Chatbot ---

@router.post("/chatbot/interacoes", response_model=InteracaoChatbotInDB, status_code=status.HTTP_201_CREATED,
             summary="Registrar nova interação do chatbot",
             description="Cria um novo registro de interação do usuário com o chatbot.")
async def create_interacao_chatbot(interacao: InteracaoChatbotCreate, db=Depends(get_db)):
    """
    Registra uma nova interação do chatbot no banco de dados.
    """
    try:
        data_to_insert = interacao.model_dump()
        response = db.table("interacoes_chatbot").insert(data_to_insert).execute()

        if response.data:
            return InteracaoChatbotInDB(**response.data[0])
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao criar interação do chatbot.")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro no servidor: {e}")

@router.get("/chatbot/interacoes", response_model=List[InteracaoChatbotInDB],
            summary="Listar interações do chatbot",
            description="Retorna uma lista de todas as interações do chatbot.")
async def read_interacoes_chatbot(db=Depends(get_db)):
    """
    Retorna todas as interações do chatbot.
    """
    try:
        response = db.table("interacoes_chatbot").select("*").order("created_at", desc=True).execute()
        return [InteracaoChatbotInDB(**item) for item in response.data]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro no servidor: {e}")

@router.get("/chatbot/interacoes/{interacao_id}", response_model=InteracaoChatbotInDB,
            summary="Obter interação do chatbot por ID",
            description="Retorna uma interação específica do chatbot pelo seu ID.")
async def read_interacao_chatbot(interacao_id: int, db=Depends(get_db)):
    """
    Retorna uma interação do chatbot pelo seu ID.
    """
    try:
        response = db.table("interacoes_chatbot").select("*").eq("id", interacao_id).single().execute()
        if response.data:
            return InteracaoChatbotInDB(**response.data)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interação do chatbot não encontrada.")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro no servidor: {e}")

# --- Endpoints de Leads Jurídicos ---

@router.post("/leads/juridicos", response_model=LeadJuridicoInDB, status_code=status.HTTP_201_CREATED,
             summary="Criar novo lead jurídico",
             description="Cria um novo lead jurídico, geralmente a partir de uma interação do chatbot, e envia notificação por e-mail.")
async def create_lead_juridico(lead: LeadJuridicoCreate, db=Depends(get_db)):
    """
    Cria um novo lead jurídico e envia uma notificação por e-mail.
    """
    try:
        data_to_insert = lead.model_dump()
        response = db.table("leads_juridicos").insert(data_to_insert).execute()

        if response.data:
            new_lead = LeadJuridicoInDB(**response.data[0])

            # Enviar e-mail de notificação (este endpoint ainda não funcionará sem as credenciais de e-mail)
            subject = f"Novo Lead Jurídico Gerado: {new_lead.nome_completo}"
            body = (
                f"Um novo lead jurídico foi gerado:\n\n"
                f"Nome: {new_lead.nome_completo}\n"
                f"Email: {new_lead.email}\n"
                f"Telefone: {new_lead.telefone or 'N/A'}\n"
                f"Tipo de Caso: {new_lead.tipo_caso or 'N/A'}\n"
                f"Descrição: {new_lead.descricao_problema}\n"
                f"Status: {new_lead.status_lead}\n"
                f"Prioridade: {new_lead.prioridade}\n"
                f"Interação ID: {new_lead.interacao_id}\n\n"
                f"Acesse o portal para mais detalhes."
            )
            # O e-mail será enviado para o EMAIL_USER configurado no .env
            # send_email(os.getenv("EMAIL_USER"), subject, body) # Descomente quando o e-mail estiver configurado
            print(f"Notificação de lead para {new_lead.email} (e-mail desativado por enquanto).")

            return new_lead
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao criar lead jurídico.")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro no servidor: {e}")

@router.get("/leads/juridicos", response_model=List[LeadJuridicoInDB],
            summary="Listar leads jurídicos",
            description="Retorna uma lista de todos os leads jurídicos.")
async def read_leads_juridicos(db=Depends(get_db)):
    """
    Retorna todos os leads jurídicos.
    """
    try:
        response = db.table("leads_juridicos").select("*").order("created_at", desc=True).execute()
        return [LeadJuridicoInDB(**item) for item in response.data]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro no servidor: {e}")

@router.get("/leads/juridicos/{lead_id}", response_model=LeadJuridicoInDB,
            summary="Obter lead jurídico por ID",
            description="Retorna um lead jurídico específico pelo seu ID.")
async def read_lead_juridico(lead_id: int, db=Depends(get_db)):
    """
    Retorna um lead jurídico pelo seu ID.
    """
    try:
        response = db.table("leads_juridicos").select("*").eq("id", lead_id).single().execute()
        if response.data:
            return LeadJuridicoInDB(**response.data)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lead jurídico não encontrado.")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro no servidor: {e}")

@router.put("/leads/juridicos/{lead_id}/status", response_model=LeadJuridicoInDB,
            summary="Atualizar status de um lead jurídico",
            description="Atualiza o status de um lead jurídico existente pelo seu ID.")
async def update_lead_juridico_status(lead_id: int, status_update: dict[str, str], db=Depends(get_db)): # <--- LINHA CORRIGIDA AQUI
    """
    Atualiza o status de um lead jurídico.
    O 'status_update' deve ser um dicionário com a chave 'status_lead'.
    Ex: {"status_lead": "Qualificado"}
    """
    if "status_lead" not in status_update:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Campo 'status_lead' é obrigatório.")

    try:
        response = db.table("leads_juridicos").update({"status_lead": status_update["status_lead"], "updated_at": datetime.now().isoformat()}).eq("id", lead_id).execute()
        if response.data:
            return LeadJuridicoInDB(**response.data[0])
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lead jurídico não encontrado.")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro no servidor: {e}")

@router.delete("/leads/juridicos/{lead_id}", status_code=status.HTTP_204_NO_CONTENT,
               summary="Deletar lead jurídico",
               description="Deleta um lead jurídico existente pelo seu ID.")
async def delete_lead_juridico(lead_id: int, db=Depends(get_db)):
    """
    Deleta um lead jurídico pelo seu ID.
    """
    try:
        response = db.table("leads_juridicos").delete().eq("id", lead_id).execute()
        # Supabase delete retorna data vazia se sucesso, ou erro se não encontrar
        # Se a operação não levantar exceção, consideramos sucesso.
        # Poderíamos verificar response.count se o Supabase retornasse, mas geralmente não retorna para delete.
        # Uma forma de verificar se realmente deletou é tentar buscar antes, mas para simplicidade, confiamos no .execute()
        return {"message": "Lead jurídico deletado com sucesso."}
    except Exception as e:
        # Se o Supabase retornar um erro 404 para item não encontrado, podemos capturar aqui
        if "PGRST" in str(e) and "404" in str(e): # Exemplo de como Supabase pode retornar 404
             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lead jurídico não encontrado.")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro no servidor: {e}")
