from service.email_channel import EmailChannel
from service.whatsapp_channel import WhatsappChannel

class MensagemService:
    def __init__(self):
        self.email_channel = EmailChannel()
        self.whatsapp_channel = WhatsappChannel()

    def enviar_mensagem(self, canal: str, destinatario: str, conteudo: str, assunto: str = None):
        """
        Envia uma mensagem pelo canal especificado.
        Retorna True se enviado com sucesso, False caso contrário.
        """
        try:
            if canal.lower() == "email":
                return self.email_channel.enviar(destinatario, assunto or "Notificação Automática", conteudo)
            elif canal.lower() == "whatsapp":
                return self.whatsapp_channel.enviar(destinatario, conteudo)
            else:
                print(f"[ERRO] Canal '{canal}' não suportado.")
                return False
        except Exception as e:
            print(f"[ERRO] Exceção ao enviar mensagem: {e}")
            return False
