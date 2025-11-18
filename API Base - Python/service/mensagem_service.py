from service.email_channel import EmailChannel
from service.whatsapp_channel import WhatsappChannel

class MensagemService:
    def __init__(self):
        self.email_channel = EmailChannel()
        self.whatsapp_channel = WhatsappChannel()
        self.last_error = None

    def enviar_mensagem(self, canal: str, destinatario: str, conteudo: str, assunto: str = None):
        """
        Envia uma mensagem pelo canal especificado.
        Retorna (True, None) se enviado com sucesso, (False, erro_msg) caso contrário.
        """
        try:
            if canal.lower() == "email":
                success = self.email_channel.enviar(destinatario, assunto or "Notificação Automática", conteudo)
                if not success:
                    self.last_error = getattr(self.email_channel, 'last_error', 'Erro desconhecido')
                return (success, self.last_error if not success else None)
            elif canal.lower() == "whatsapp":
                success = self.whatsapp_channel.enviar(destinatario, conteudo)
                if not success:
                    self.last_error = getattr(self.whatsapp_channel, 'last_error', 'Erro desconhecido')
                return (success, self.last_error if not success else None)
            else:
                msg = f"Canal '{canal}' não suportado."
                print(f"[ERRO] {msg}")
                self.last_error = msg
                return (False, msg)
        except Exception as e:
            msg = str(e)
            print(f"[ERRO] Exceção ao enviar mensagem: {e}")
            self.last_error = msg
            return (False, msg)
