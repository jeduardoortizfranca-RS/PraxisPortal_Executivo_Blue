# backend/utils/email_service.py
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações do servidor de e-mail (Gmail como exemplo)
# Você pode usar outro provedor, apenas ajuste as variáveis
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587)) # 587 para TLS, 465 para SSL
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD") # Senha do aplicativo ou senha normal

async def send_email(to_email: str, subject: str, body: str):
    """
    Envia um e-mail usando as configurações do ambiente.
    """
    if not EMAIL_USER or not EMAIL_PASSWORD:
        print("AVISO: Variáveis de ambiente EMAIL_USER ou EMAIL_PASSWORD não configuradas. E-mail não será enviado.")
        return False

    try: # <--- O BLOCO 'try' COMEÇA AQUI
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls() # Inicia a criptografia TLS
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.send_message(msg)
        print(f"E-mail enviado com sucesso para {to_email} com o assunto: {subject}")
        return True
    except Exception as e: # <--- E O 'except' CAPTURA ERROS AQUI
        print(f"ERRO ao enviar e-mail para {to_email}: {e}")
        return False

# Exemplo de uso (apenas para teste, não será executado automaticamente)
# if __name__ == "__main__":
#     import asyncio
#     async def test_send():
#         await send_email("destinatario@example.com", "Teste de E-mail Praxis AI", "Este é um e-mail de teste do serviço Praxis AI.")
#     asyncio.run(test_send())
