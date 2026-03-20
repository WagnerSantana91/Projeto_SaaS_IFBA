import logging

from django.conf import settings
from django.core.mail import send_mail

from apps.empresas.models import Empresa

logger = logging.getLogger(__name__)


def _destinatarios_notificacao():
    destinatarios = list(
        Empresa.objects.filter(esta_ativo=True)
        .exclude(email='')
        .values_list('email', flat=True)
    )

    for email in getattr(settings, 'NOTIFICATION_EMAILS', []):
        if email not in destinatarios:
            destinatarios.append(email)

    return destinatarios


def enviar_email_notificacao(assunto, mensagem):
    destinatarios = _destinatarios_notificacao()
    if not destinatarios:
        logger.warning('Nenhum destinatario de e-mail configurado para notificacoes.')
        return False

    send_mail(
        subject=assunto,
        message=mensagem,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=destinatarios,
        fail_silently=True,
    )
    return True
