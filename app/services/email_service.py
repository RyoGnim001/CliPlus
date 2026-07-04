import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from settings.config import MAIL_EMAIL, MAIL_SENHA

def enviar_comprovante(destinatario: str, nome_paciente: str, pdf_bytes: bytes, consulta_id: int):
    msg = MIMEMultipart()
    msg["From"]     = f"Clínica Saúde & Vida <{MAIL_EMAIL}>"
    msg["To"]       = destinatario
    msg["Reply-To"] = f"noreply <{MAIL_EMAIL}>"
    msg["Subject"]  = "Comprovante de Consulta — Clínica Saúde & Vida"

    corpo = f"""
Olá, {nome_paciente}!


Segue em anexo o comprovante da sua consulta registrada na Clínica Saúde & Vida.

Este é um email automático, por favor não responda.
Caso tenha alguma dúvida, entre em contato pelo telefone (83) 98755-9076.

Atenciosamente,
Equipe Clínica Saúde & Vida
Rua Coronel Adauto, 142 — Centro, Guarabira — PB
    """
    msg.attach(MIMEText(corpo, "plain", "utf-8"))

    anexo = MIMEBase("application", "octet-stream")
    anexo.set_payload(pdf_bytes)
    encoders.encode_base64(anexo)
    anexo.add_header("Content-Disposition", f"attachment; filename=comprovante_{consulta_id}.pdf")
    msg.attach(anexo)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(MAIL_EMAIL, MAIL_SENHA)
        smtp.sendmail(MAIL_EMAIL, destinatario, msg.as_string())