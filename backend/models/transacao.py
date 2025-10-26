
from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from ..database import Base

class Transacao(Base):
    __tablename__ = "transacoes"
    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String, nullable=False)
    categoria = Column(String, nullable=True)
    valor = Column(Float, nullable=False)
    criado_em = Column(DateTime, default=datetime.utcnow)
