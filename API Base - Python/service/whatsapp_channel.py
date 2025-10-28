from twilio.rest import Client

class WhatsappChannel:
    def enviar(self, numero: str, conteudo: str):
        account_sid = "SEU_ACCOUNT_SID"
        auth_token = "SEU_AUTH_TOKEN"
        from_whatsapp = "whatsapp:+14155238886"  # número Twilio

        client = Client(account_sid, auth_token)

        try:
            client.messages.create(
                body=conteudo,
                from_=from_whatsapp,
                to=f"whatsapp:{numero}"
            )
            print(f"[WHATSAPP] Mensagem enviada para {numero}")
            return True
        except Exception as e:
            print(f"[WHATSAPP] Erro ao enviar: {e}")
            return False
