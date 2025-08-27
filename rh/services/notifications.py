from django.core.mail import send_mail
from django.conf import settings


def notificar_admissao(obj, usuario):
    send_mail(
        subject="📥 Nova admissão registrada",
        message=(
            f"Uma nova admissão foi registrada:\n\n"
            f"Nome: {obj.nome}\n"
            f"Código RCA: {obj.codigo}\n"
            f"Data de Admissão: {obj.data_admissao.strftime('%d/%m/%Y') if obj.data_admissao else '-'}\n"
            f"Cargo: {obj.cargo or '-'}\n"
            f"Supervisor Responsável: {obj.supervisor_responsavel or '-'}\n"
            f"Registrado por: {usuario.get_username()}"
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=["rh@omegadistribuidora.com.br"],
    )


def notificar_desligamento(obj, usuario):
    send_mail(
        subject="📤 Novo desligamento registrado",
        message=(
            f"Um novo desligamento foi registrado:\n\n"
            f"Nome: {obj.nome}\n"
            f"Código: {obj.codigo}\n"
            f"Área: {obj.area_atuacao}\n"
            f"Data de Demissão: {obj.demissao.strftime('%d/%m/%Y') if obj.demissao else '-'}\n"
            f"Registrado por: {usuario.get_username()}"
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=["rh@omegadistribuidora.com.br"],
    )
