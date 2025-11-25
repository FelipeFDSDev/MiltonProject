from fastapi import APIRouter, Query, HTTPException, Depends, status
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime, timezone
import pytz

from database import SessionLocal, MensagemAgendada, User
from models import MensagemAgendadaCreate, MensagemAgendadaUpdate, MensagemAgendadaOut
from auth import get_current_active_user
from dependencies import get_db
from service.agendamento_service import AgendamentoService

router = APIRouter(prefix="/agendamentos", tags=["Agendamentos"])


@router.post("/", response_model=MensagemAgendadaOut, status_code=status.HTTP_201_CREATED)
async def criar_agendamento(
    mensagem: MensagemAgendadaCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    try:
        print(f"Recebida solicitação para criar agendamento: {mensagem}")
        
        # Busca o contato no banco de dados
        from database import Contact
        
        print(f"Buscando contato com ID: {mensagem.contact_id}")
        contato = db.query(Contact).filter(Contact.id == mensagem.contact_id).first()
        
        if not contato:
            error_msg = f"Contato com ID {mensagem.contact_id} não encontrado"
            print(error_msg)
            raise HTTPException(status_code=404, detail=error_msg)
        
        print(f"Contato encontrado: {contato.name} ({contato.email})")
        
        # Define o destinatário com base no canal escolhido
        canal = mensagem.canal.lower()
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

        # Valida se a data de agendamento é futura
        tz = pytz.timezone('America/Sao_Paulo')
        agora = datetime.now(tz)
        
        # Garante que a data de agendamento está no fuso horário correto
        data_agendamento = mensagem.data_agendamento
        if data_agendamento.tzinfo is None:
            data_agendamento = tz.localize(data_agendamento)
        
        if data_agendamento <= agora:
            error_msg = f"A data de agendamento deve ser no futuro. Data atual: {agora}, Data fornecida: {data_agendamento}"
            print(error_msg)
            raise HTTPException(status_code=400, detail=error_msg)
        
        # Cria o agendamento no banco
        print(f"Criando agendamento para {destinatario} no canal {canal}")
        db_mensagem = MensagemAgendada(
            canal=canal,
            destinatario=destinatario,
            assunto=mensagem.assunto,
            conteudo=mensagem.conteudo,
            data_agendamento=data_agendamento,
            contato_id=contato.id
        )
        
        db.add(db_mensagem)
        db.commit()
        db.refresh(db_mensagem)
        
        print(f"Agendamento criado com sucesso: ID {db_mensagem.id}")
        return db_mensagem
        
    except HTTPException:
        # Re-lança exceções HTTP que já foram tratadas
        raise
    except Exception as e:
        # Captura outros erros inesperados
        error_msg = f"Erro ao criar agendamento: {str(e)}"
        print(error_msg)
        db.rollback()  # Desfaz qualquer alteração no banco de dados
        raise HTTPException(
            status_code=500,
            detail=error_msg
        )


@router.get("/", response_model=List[MensagemAgendadaOut])
async def listar_agendamentos(
    status: str = None,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
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

@router.get("/consulta", response_model=List[MensagemAgendadaOut])
async def consulta_agendamentos(
    contact_id: Optional[int] = None,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Consulta agendamentos filtrando por ID do contato e/ou status.
    
    Parâmetros:
    - **contact_id**: ID do contato para filtrar os agendamentos
    - **status**: Status para filtrar (AGENDADO, ENVIADO, CANCELADO, ERRO)
    - **skip**: Número de registros para pular (paginação)
    - **limit**: Número máximo de registros a retornar (padrão: 100)
    """
    query = db.query(MensagemAgendada)

    if contact_id is not None:
        query = query.filter(MensagemAgendada.contato_id == contact_id)
    if status:
        query = query.filter(MensagemAgendada.status == status.upper())

    resultados = query.order_by(MensagemAgendada.data_agendamento.desc()).offset(skip).limit(limit).all()
    return resultados

@router.get("/{agendamento_id}", response_model=MensagemAgendadaOut)
async def obter_agendamento(
    agendamento_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Obtém detalhes de um agendamento específico.
    """
    mensagem = db.query(MensagemAgendada).filter(MensagemAgendada.id == agendamento_id).first()
    
    if not mensagem:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado.")
    
    return mensagem


@router.put("/{agendamento_id}", response_model=MensagemAgendadaOut)
async def atualizar_agendamento(
    agendamento_id: int,
    mensagem_update: MensagemAgendadaUpdate,
    current_user: User = Depends(get_current_active_user),
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


@router.delete("/{agendamento_id}", status_code=status.HTTP_204_NO_CONTENT)
async def cancelar_agendamento(
    agendamento_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
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
async def listar_agendamentos_ativos(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Lista apenas os agendamentos ativos (status AGENDADO).
    Ordenados por data de agendamento.
    """
    service = AgendamentoService()
    return service.obter_agendamentos_ativos(db)


@router.post("/processar/manual", status_code=status.HTTP_200_OK)
async def processar_agendamentos_manual(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
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


