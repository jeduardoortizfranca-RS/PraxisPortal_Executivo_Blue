# backend/models/lead.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class LeadCreate(BaseModel):
    """
    Modelo Pydantic para criar um novo lead.
    Corresponde aos dados que o cliente envia para criar um lead.
    """
    name: str = Field(..., description="Nome do lead")
    email: EmailStr = Field(..., description="Email do lead")
    phone: Optional[str] = Field(None, description="Telefone do lead")
    company: Optional[str] = Field(None, description="Empresa do lead")
    source: Optional[str] = Field(None, description="Origem do lead (ex: 'website', 'referral')")
    status: Optional[str] = Field("New", description="Status atual do lead (ex: 'New', 'Contacted', 'Qualified')")

class LeadResponse(LeadCreate):
    """
    Modelo Pydantic para resposta de lead.
    Inclui campos gerados pelo backend, como ID e timestamp.
    """
    id: str = Field(..., description="ID único do lead")
    created_at: datetime = Field(..., description="Data e hora de criação do lead")
    updated_at: Optional[datetime] = Field(None, description="Data e hora da última atualização do lead")
    class Config:
        from_attributes = True # Permite que o Pydantic leia atributos de objetos ORM
