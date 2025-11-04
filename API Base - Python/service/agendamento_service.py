from datetime import datetime
from sqlalchemy.orm import Session
from models import MensagemAgendada
from service.mensagem_service import MensagemService
from database import SessionLocal


class AgendamentoService:
    """
    Serviço responsável por processar mensagens agendadas.
    """
    
    def __init__(self):
        self.mensagem_service = MensagemService()
    
    def processar_mensagens_pendentes(self):
        """
        Busca e processa todas as mensagens agendadas que já passaram do horário.
        Retorna o número de mensagens processadas.
        """
        db: Session = SessionLocal()
        try:
            agora = datetime.utcnow()
            mensagens_pendentes = db.query(MensagemAgendada).filter(
                MensagemAgendada.status == "AGENDADO",
                MensagemAgendada.data_agendamento <= agora
            ).all()
            
            processadas = 0
            for mensagem in mensagens_pendentes:
                try:
                    sucesso = self.mensagem_service.enviar_mensagem(
                        canal=mensagem.canal,
                        destinatario=mensagem.destinatario,
                        conteudo=mensagem.conteudo,
                        assunto=mensagem.assunto
                    )
                    
                    if sucesso:
                        mensagem.status = "ENVIADO"
                        mensagem.enviado_em = datetime.utcnow()
                        print(f"[AGENDAMENTO] Mensagem {mensagem.id} enviada com sucesso.")
                    else:
                        mensagem.status = "ERRO"
                        mensagem.erro_mensagem = "Falha no envio da mensagem"
                        print(f"[AGENDAMENTO] Erro ao enviar mensagem {mensagem.id}.")
                    
                    processadas += 1
                    
                except Exception as e:
                    mensagem.status = "ERRO"
                    mensagem.erro_mensagem = str(e)
                    print(f"[AGENDAMENTO] Exceção ao processar mensagem {mensagem.id}: {e}")
                
                db.commit()
            
            return processadas
            
        except Exception as e:
            print(f"[AGENDAMENTO] Erro ao processar mensagens: {e}")
            return 0
        finally:
            db.close()
    
    def cancelar_agendamento(self, mensagem_id: int, db: Session) -> bool:
        """
        Cancela um agendamento específico.
        """
        mensagem = db.query(MensagemAgendada).filter(MensagemAgendada.id == mensagem_id).first()
        if not mensagem:
            return False
        
        if mensagem.status != "AGENDADO":
            return False
        
        mensagem.status = "CANCELADO"
        db.commit()
        return True
    
    def obter_agendamentos_ativos(self, db: Session):
        """
        Retorna todos os agendamentos com status AGENDADO.
        """
        return db.query(MensagemAgendada).filter(
            MensagemAgendada.status == "AGENDADO"
        ).order_by(MensagemAgendada.data_agendamento).all()

    def listar_agendamentos(self):
        """
        Retorna todos os agendamentos cadastrados.
        """
        db: Session = SessionLocal()
        try:
            return db.query(MensagemAgendada).all()
        finally:
            db.close()

