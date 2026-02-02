from typing import Dict
from agents import function_tool
import resend
import os

resend.api_key = os.getenv("RESEND_API_KEY")

@function_tool
def send_email(subject: str, html: str, to: str = "miguel.ossa.abellan@gmail.com") -> Dict[str, str]:
    """Envía un email con el asunto y cuerpo HTML dados"""
    r = resend.Emails.send({
        "from": "onboarding@resend.dev",
        "to": to,
        "subject": subject,
        "html": html
    })
    return {"estado": "exito"}
