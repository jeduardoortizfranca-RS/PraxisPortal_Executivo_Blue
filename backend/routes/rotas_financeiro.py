
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.transacao import Transacao

router = APIRouter(prefix="/financeiro", tags=["Financeiro"])

class NovaTransacao(BaseModel):
    descricao: str = Field(..., min_length=2, max_length=160)
    valor: float
    categoria: str | None = None

class TransacaoOut(BaseModel):
    id: int
    descricao: str
    categoria: str | None
    valor: float
    class Config:
        from_attributes = True

@router.get("/transacoes", response_model=List[TransacaoOut])
def listar_transacoes(db: Session = Depends(get_db)):
    itens = db.query(Transacao).order_by(Transacao.criado_em.desc()).all()
    return itens

@router.post("/nova")
def criar_transacao(payload: NovaTransacao, db: Session = Depends(get_db)):
    t = Transacao(descricao=payload.descricao, categoria=payload.categoria, valor=payload.valor)
    db.add(t); db.commit(); db.refresh(t)
    saldo = db.query(Transacao).with_entities((Transacao.valor).label("v")).all()
    saldo_total = sum(v for (v,) in saldo)
    return {"mensagem": "Transação adicionada com sucesso", "id": t.id, "descricao": t.descricao, "valor": t.valor, "saldo_total": round(saldo_total, 2)}

@router.delete("/remover/{id}")
def remover_transacao(id: int, db: Session = Depends(get_db)):
    t = db.query(Transacao).filter(Transacao.id == id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Transação não encontrada")
    db.delete(t); db.commit()
    saldo = db.query(Transacao).with_entities((Transacao.valor).label("v")).all()
    saldo_total = sum(v for (v,) in saldo)
    return {"mensagem": "Transação removida", "saldo_total": round(saldo_total, 2)}

@router.get("/resumo")
def resumo_financeiro(db: Session = Depends(get_db)):
    linhas = db.query(Transacao).with_entities((Transacao.valor).label("v")).all()
    saldo_total = sum(v for (v,) in linhas)
    qtd = db.query(Transacao).count()
    return {"qtd_transacoes": qtd, "saldo_total": round(saldo_total, 2)}
