import smtplib
from email.mime.text import MIMEText
import os


class EmailChannel:
    def __init__(self):
        self.last_error = None
    
    def enviar(self, destinatario: str, assunto: str, conteudo: str):
        remetente = os.getenv("EMAIL_USER")
        senha = os.getenv("EMAIL_PASS")

        # Ler configurações SMTP do ambiente (fallback para Gmail)
        smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        try:
            smtp_port = int(os.getenv("SMTP_PORT", "587"))
        except ValueError:
            smtp_port = 587

        use_tls = os.getenv("SMTP_USE_TLS", "True").lower() in ("1", "true", "yes")

        # Validação básica
        if not remetente or not senha:
            msg = "EMAIL_USER ou EMAIL_PASS não configurados no .env"
            self.last_error = msg
            print(f"[EMAIL] Erro: {msg}")
            return False

        msg_obj = MIMEText(conteudo, "plain", "utf-8")
        msg_obj["Subject"] = assunto
        msg_obj["From"] = remetente
        msg_obj["To"] = destinatario

        try:
            with smtplib.SMTP(smtp_host, smtp_port, timeout=20) as server:
                if use_tls:
                    server.starttls()
                server.login(remetente, senha)
                server.send_message(msg_obj)
            print(f"[EMAIL] Mensagem enviada para {destinatario} via {smtp_host}:{smtp_port}")
            self.last_error = None
            return True
        except Exception as e:
            # Logar erro completo para diagnóstico
            err_msg = str(e)
            print(f"[EMAIL] Erro ao enviar: {err_msg}")
            self.last_error = err_msg
            return False
