# backend/models/transaction.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TransactionCreate(BaseModel):
    """
    Modelo Pydantic para criar uma nova transação.
    Corresponde aos dados que o cliente envia para criar uma transação.
    """
    amount: float = Field(..., description="Valor da transação")
    description: Optional[str] = Field(None, description="Descrição da transação")
    type: str = Field(..., description="Tipo da transação (ex: 'income', 'expense')")
    category: Optional[str] = Field(None, description="Categoria da transação")
    # user_id não é incluído aqui, pois será inferido do token de autenticação

class TransactionResponse(TransactionCreate):
    """
    Modelo Pydantic para resposta de transação.
    Inclui campos gerados pelo backend, como ID e timestamp.
    """
    id: str = Field(..., description="ID único da transação")
    user_id: str = Field(..., description="ID do usuário associado à transação")
    created_at: datetime = Field(..., description="Data e hora de criação da transação")
    class Config:
        from_attributes = True # Permite que o Pydantic leia atributos de objetos ORM

