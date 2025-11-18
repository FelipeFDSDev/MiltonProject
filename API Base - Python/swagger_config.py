"""
Configuração personalizada para o Swagger UI.
"""

def swagger_ui_settings():
    return {
        "swagger": "2.0",
        "info": {
            "title": "Microserviço de Agendamento e Comunicação",
            "description": "Gerencia contatos, envio e agendamento de mensagens.",
            "version": "1.0.0"
        },
        "securityDefinitions": {
            "OAuth2PasswordBearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "Insira o token JWT no formato: Bearer <token>"
            }
        },
        "security": [
            {
                "OAuth2PasswordBearer": []
            }
        ]
    }
