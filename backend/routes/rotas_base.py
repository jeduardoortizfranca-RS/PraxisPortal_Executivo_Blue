
from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/status")
def status():
    return {"ok": True, "app": "Núcleo de IA Praxis", "hora": datetime.utcnow().isoformat() + "Z"}
