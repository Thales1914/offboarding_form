from django.db import models
from django.contrib.auth.models import User

class Desligamento(models.Model):
    codigo = models.CharField("Código", max_length=20)
    nome = models.CharField("Nome", max_length=100)
    contato = models.CharField("Contato Particular", max_length=50, blank=True, null=True)
    admissao = models.DateField("Admissão")
    demissao = models.DateField("Demissão")
    area_atuacao = models.CharField("Área de Atuação", max_length=100)

    motivo = models.TextField("Motivo do Desligamento", blank=True, null=True)

    fardamento = models.BooleanField("Fardamento", default=False)
    chip_voz = models.BooleanField("Chip de Voz", default=False)
    chip_dados = models.BooleanField("Chip de Dados", default=False)
    tablet = models.BooleanField("Tablet", default=False)
    carregador_tablet = models.BooleanField("Carregador do Tablet", default=False)
    fone_tablet = models.BooleanField("Fone de Ouvido do Tablet", default=False)
    catalogo = models.BooleanField("Catálogo", default=False)
    bloco_pedido = models.BooleanField("Bloco de Pedido", default=False)
    carta_pedido_demissao = models.BooleanField("Carta de Pedido de Demissão", default=False)
    relatorio_inadimplencia = models.BooleanField("Relatório de Inadimplência", default=False)

    substituto = models.BooleanField("Há substituto em seleção?", default=False)
    telemarketing = models.BooleanField("Área liberada para Telemarketing?", default=False)
    nova_contratacao = models.BooleanField("Há previsão de nova contratação?", default=False)

    observacoes = models.TextField("Observações", blank=True, null=True)

    data_registro = models.DateField("Data de Registro", auto_now_add=True)

    criado_por = models.ForeignKey(
        User,
        verbose_name="Criado por",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Desligamento"
        verbose_name_plural = "Desligamentos"

    def __str__(self):
        return f"{self.nome} ({self.codigo})"

    @property
    def supervisor(self):

        return self.criado_por.first_name or self.criado_por.username if self.criado_por else "—"
