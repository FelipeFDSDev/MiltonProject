from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from datetime import datetime

from database import SessionLocal
from models import MensagemAgendada, MensagemAgendadaCreate, MensagemAgendadaUpdate, MensagemAgendadaOut
from service.agendamento_service import AgendamentoService

router = APIRouter(prefix="/agendamentos", tags=["Agendamentos"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=MensagemAgendadaOut, status_code=201)
def criar_agendamento(mensagem: MensagemAgendadaCreate, db: Session = Depends(get_db)):
    """
    Cria um novo agendamento de mensagem.
    
    Exemplo:
    ```json
    {
        "canal": "email",
        "destinatario": "cliente@teste.com",
        "assunto": "Lembrete",
        "conteudo": "Sua consulta é amanhã às 14h",
        "data_agendamento": "2025-11-03T14:00:00"
    }
    ```
    """
    # Valida se a data de agendamento é futura
    if mensagem.data_agendamento <= datetime.utcnow():
        raise HTTPException(
            status_code=400, 
            detail="A data de agendamento deve ser no futuro."
        )
    
    # Valida o canal
    if mensagem.canal.lower() not in ["email", "whatsapp"]:
        raise HTTPException(
            status_code=400,
            detail="Canal inválido. Use 'email' ou 'whatsapp'."
        )
    
    # Cria o agendamento no banco
    db_mensagem = MensagemAgendada(**mensagem.model_dump())
    db.add(db_mensagem)
    db.commit()
    db.refresh(db_mensagem)
    
    return db_mensagem


@router.get("/", response_model=List[MensagemAgendadaOut])
def listar_agendamentos(
    status: str = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Lista todos os agendamentos.
    
    Parâmetros:
    - **status**: Filtra por status (AGENDADO, ENVIADO, CANCELADO, ERRO)
    - **skip**: Número de registros para pular (paginação)
    - **limit**: Número máximo de registros a retornar
    """
    query = db.query(MensagemAgendada)
    
    if status:
        query = query.filter(MensagemAgendada.status == status.upper())
    
    mensagens = query.order_by(MensagemAgendada.data_agendamento.desc()).offset(skip).limit(limit).all()
    return mensagens


@router.get("/{agendamento_id}", response_model=MensagemAgendadaOut)
def obter_agendamento(agendamento_id: int, db: Session = Depends(get_db)):
    """
    Obtém detalhes de um agendamento específico.
    """
    mensagem = db.query(MensagemAgendada).filter(MensagemAgendada.id == agendamento_id).first()
    
    if not mensagem:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado.")
    
    return mensagem


@router.put("/{agendamento_id}", response_model=MensagemAgendadaOut)
def atualizar_agendamento(
    agendamento_id: int,
    mensagem_update: MensagemAgendadaUpdate,
    db: Session = Depends(get_db)
):
    """
    Atualiza um agendamento existente.
    Só é possível atualizar agendamentos com status AGENDADO.
    """
    mensagem = db.query(MensagemAgendada).filter(MensagemAgendada.id == agendamento_id).first()
    
    if not mensagem:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado.")
    
    if mensagem.status != "AGENDADO":
        raise HTTPException(
            status_code=400,
            detail=f"Não é possível atualizar agendamento com status '{mensagem.status}'."
        )
    
    # Atualiza apenas os campos fornecidos
    update_data = mensagem_update.model_dump(exclude_unset=True)
    
    # Valida data de agendamento se fornecida
    if "data_agendamento" in update_data and update_data["data_agendamento"]:
        if update_data["data_agendamento"] <= datetime.utcnow():
            raise HTTPException(
                status_code=400,
                detail="A data de agendamento deve ser no futuro."
            )
    
    for key, value in update_data.items():
        setattr(mensagem, key, value)
    
    db.commit()
    db.refresh(mensagem)
    
    return mensagem


@router.delete("/{agendamento_id}", status_code=200)
def cancelar_agendamento(agendamento_id: int, db: Session = Depends(get_db)):
    """
    Cancela um agendamento.
    Só é possível cancelar agendamentos com status AGENDADO.
    """
    service = AgendamentoService()
    sucesso = service.cancelar_agendamento(agendamento_id, db)
    
    if not sucesso:
        mensagem = db.query(MensagemAgendada).filter(MensagemAgendada.id == agendamento_id).first()
        if not mensagem:
            raise HTTPException(status_code=404, detail="Agendamento não encontrado.")
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Não é possível cancelar agendamento com status '{mensagem.status}'."
            )
    
    return {"status": "cancelado", "id": agendamento_id}


@router.get("/ativos/listar", response_model=List[MensagemAgendadaOut])
def listar_agendamentos_ativos(db: Session = Depends(get_db)):
    """
    Lista apenas os agendamentos ativos (status AGENDADO).
    Ordenados por data de agendamento.
    """
    service = AgendamentoService()
    return service.obter_agendamentos_ativos(db)


@router.post("/processar/manual", status_code=200)
def processar_agendamentos_manual(db: Session = Depends(get_db)):
    """
    Processa manualmente as mensagens agendadas que já passaram do horário.
    Útil para testes ou processamento forçado.
    """
    service = AgendamentoService()
    processadas = service.processar_mensagens_pendentes()
    
    return {
        "status": "processado",
        "mensagens_processadas": processadas
    }
