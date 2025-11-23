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
    contact_id: int,
    conteudo: str,
    assunto: Optional[str] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Busca o contato no banco de dados
    from database import Contact
    
    print(f"Buscando contato com ID: {contact_id}")
    contato = db.query(Contact).filter(Contact.id == contact_id).first()
    
    if not contato:
        error_msg = f"Contato com ID {contact_id} não encontrado"
        print(error_msg)
        raise HTTPException(status_code=404, detail=error_msg)
    
    print(f"Contato encontrado: {contato.name} ({contato.email})")
    
    # Define o destinatário com base no canal escolhido
    canal = canal.lower()
    if canal == "email":
        destinatario = contato.email
        if not destinatario:
            error_msg = f"O contato {contato.name} não possui um e-mail cadastrado"
            print(error_msg)
            raise HTTPException(status_code=400, detail=error_msg)
    elif canal == "whatsapp":
        destinatario = contato.phone
        if not destinatario:
            error_msg = f"O contato {contato.name} não possui um telefone cadastrado"
            print(error_msg)
            raise HTTPException(status_code=400, detail=error_msg)
    else:
        error_msg = "Canal inválido. Use 'email' ou 'whatsapp'."
        print(error_msg)
        raise HTTPException(status_code=400, detail=error_msg)
    
    # Envia a mensagem
    service = MensagemService()
    ok, error_msg = service.enviar_mensagem(canal, destinatario, conteudo, assunto)
    if not ok:
        # Retornar erro detalhado para debug
        detail = error_msg or "Falha ao enviar mensagem."
        raise HTTPException(status_code=500, detail=detail)
    
    return {
        "status": "enviado", 
        "canal": canal, 
        "destinatario": destinatario,
        "contato_id": contato.id,
        "nome_contato": contato.name
    }

@router.post("/agendar/")
async def agendar_mensagem(
    canal: str,
    contact_id: int,
    conteudo: str,
    minutos: int = 1,
    assunto: Optional[str] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Busca o contato no banco de dados
    from database import Contact
    
    print(f"Buscando contato com ID: {contact_id}")
    contato = db.query(Contact).filter(Contact.id == contact_id).first()
    
    if not contato:
        error_msg = f"Contato com ID {contact_id} não encontrado"
        print(error_msg)
        raise HTTPException(status_code=404, detail=error_msg)
    
    print(f"Contato encontrado: {contato.name} ({contato.email})")
    
    # Define o destinatário com base no canal escolhido
    canal = canal.lower()
    if canal == "email":
        destinatario = contato.email
        if not destinatario:
            error_msg = f"O contato {contato.name} não possui um e-mail cadastrado"
            print(error_msg)
            raise HTTPException(status_code=400, detail=error_msg)
    elif canal == "whatsapp":
        destinatario = contato.phone
        if not destinatario:
            error_msg = f"O contato {contato.name} não possui um telefone cadastrado"
            print(error_msg)
            raise HTTPException(status_code=400, detail=error_msg)
    else:
        error_msg = "Canal inválido. Use 'email' ou 'whatsapp'."
        print(error_msg)
        raise HTTPException(status_code=400, detail=error_msg)
    
    # Agenda o envio da mensagem
    agendar_envio.apply_async(
        args=[canal, destinatario, conteudo, assunto], 
        countdown=minutos * 60
    )
    
    return {
        "status": "agendado", 
        "execucao_em": f"{minutos} minuto(s)",
        "canal": canal,
        "contato_id": contato.id,
        "nome_contato": contato.name,
        "destinatario": destinatario
    }
