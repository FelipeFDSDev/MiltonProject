from fastapi import APIRouter, HTTPException, Depends, status
from typing import Optional
from sqlalchemy.orm import Session

from database import SessionLocal, User
from auth import get_current_active_user
from dependencies import get_db
from service.mensagem_service import MensagemService
from service.scheduler import agendar_envio

router = APIRouter(prefix="/mensagens", tags=["Mensagens"])

@router.post("/enviar/")
async def enviar_mensagem(
    canal: str,
    destinatario: str,
    conteudo: str,
    assunto: Optional[str] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    service = MensagemService()
    ok, error_msg = service.enviar_mensagem(canal, destinatario, conteudo, assunto)
    if not ok:
        # Retornar erro detalhado para debug
        detail = error_msg or "Falha ao enviar mensagem."
        raise HTTPException(status_code=500, detail=detail)
    return {"status": "enviado", "canal": canal, "destinatario": destinatario}

@router.post("/agendar/")
async def agendar_mensagem(
    canal: str,
    destinatario: str,
    conteudo: str,
    minutos: int = 1,
    assunto: Optional[str] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    agendar_envio.apply_async(args=[canal, destinatario, conteudo, assunto], countdown=minutos * 60)
    return {"status": "agendado", "execução_em": f"{minutos} minuto(s)"}
