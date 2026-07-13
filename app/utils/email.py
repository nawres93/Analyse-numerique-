"""
Envoi d'emails avec fastapi-mail.

Note pour Noussa :
-------------------
En développement, tu n'es pas obligée d'avoir un vrai serveur SMTP tout de
suite. Si MAIL_USERNAME est vide dans le .env, les emails sont juste
affichés dans la console au lieu d'être réellement envoyés, ce qui te
permet de développer/tester sans configurer Gmail immédiatement.
"""

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from app.core.config import settings

_mail_conf = None
_fast_mail = None


def _get_fast_mail() -> FastMail | None:
    global _mail_conf, _fast_mail
    if not settings.MAIL_USERNAME or not settings.MAIL_SERVER:
        return None  # mode "console" (voir send_email ci-dessous)

    if _fast_mail is None:
        _mail_conf = ConnectionConfig(
            MAIL_USERNAME=settings.MAIL_USERNAME,
            MAIL_PASSWORD=settings.MAIL_PASSWORD,
            MAIL_FROM=settings.MAIL_FROM,
            MAIL_PORT=settings.MAIL_PORT,
            MAIL_SERVER=settings.MAIL_SERVER,
            MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
            MAIL_STARTTLS=True,
            MAIL_SSL_TLS=False,
            USE_CREDENTIALS=True,
        )
        _fast_mail = FastMail(_mail_conf)
    return _fast_mail


async def send_email(to: str, subject: str, html_body: str) -> None:
    fast_mail = _get_fast_mail()

    if fast_mail is None:
        # Mode développement sans SMTP configuré : on affiche dans la console.
        print(f"\n--- [EMAIL SIMULÉ] ---\nÀ: {to}\nSujet: {subject}\n{html_body}\n----------------------\n")
        return

    message = MessageSchema(
        subject=subject,
        recipients=[to],
        body=html_body,
        subtype=MessageType.html,
    )
    await fast_mail.send_message(message)


async def send_verification_email(to: str, token: str) -> None:
    link = f"{settings.FRONTEND_URL}/verify-email?token={token}"
    await send_email(
        to=to,
        subject="Vérifie ton adresse email",
        html_body=f"""
        <p>Bonjour,</p>
        <p>Merci de confirmer ton adresse email en cliquant sur le lien ci-dessous :</p>
        <p><a href="{link}">{link}</a></p>
        <p>Ce lien est valable une seule fois.</p>
        """,
    )


async def send_reset_password_email(to: str, token: str) -> None:
    link = f"{settings.FRONTEND_URL}/reset-password?token={token}"
    await send_email(
        to=to,
        subject="Réinitialisation de ton mot de passe",
        html_body=f"""
        <p>Bonjour,</p>
        <p>Tu as demandé une réinitialisation de mot de passe. Clique sur le lien
        ci-dessous (valable 30 minutes) :</p>
        <p><a href="{link}">{link}</a></p>
        <p>Si tu n'es pas à l'origine de cette demande, ignore cet email.</p>
        """,
    )
