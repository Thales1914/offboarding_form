from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

numero_validator = RegexValidator(r'^\d+$', 'Apenas números são permitidos.')


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


class Admissao(models.Model):
    codigo = models.CharField("Código RCA", max_length=20)
    nome = models.CharField("Nome", max_length=150)
    nascimento = models.DateField("Nascimento", null=True, blank=True)
    naturalidade = models.CharField("Naturalidade", max_length=100, blank=True, null=True)
    uf = models.CharField("UF", max_length=2, blank=True, null=True)
    mae = models.CharField("Mãe", max_length=150, blank=True, null=True)
    pai = models.CharField("Pai", max_length=150, blank=True, null=True)

    endereco = models.CharField("Endereço", max_length=200, blank=True, null=True)
    bairro = models.CharField("Bairro", max_length=100, blank=True, null=True)
    cidade = models.CharField("Cidade", max_length=100, blank=True, null=True)
    estado = models.CharField("Estado", max_length=2, blank=True, null=True)
    cep = models.CharField("CEP", max_length=10, blank=True, null=True)

    fone = models.CharField("Telefone", max_length=20, blank=True, null=True)
    email = models.EmailField("Email", blank=True, null=True)

    rg = models.CharField("RG", max_length=20, blank=True, null=True)
    orgao_exp = models.CharField("Órgão Expedidor", max_length=20, blank=True, null=True)
    emissao = models.DateField("Data de Emissão RG", null=True, blank=True)
    cpf = models.CharField("CPF", max_length=14, blank=True, null=True)

    banco = models.CharField("Banco", max_length=100, blank=True, null=True)
    agencia = models.CharField("Agência", max_length=20, blank=True, null=True)
    conta = models.CharField("Conta", max_length=20, blank=True, null=True)
    operacao = models.CharField("Operação", max_length=10, blank=True, null=True)

    data_admissao = models.DateField("Data de Admissão", null=True, blank=True)
    cargo = models.CharField("Cargo a Ocupar", max_length=100, blank=True, null=True)
    substituicao = models.BooleanField("É substituição?", default=False)

    supervisor_responsavel = models.CharField("Supervisor Responsável", max_length=100, blank=True, null=True)
    coordenador = models.CharField("Coordenador", max_length=100, blank=True, null=True)

    conta_gov = models.CharField("Conta Gov", max_length=100, blank=True, null=True)
    senha_gov = models.CharField("Senha Gov", max_length=100, blank=True, null=True)

    observacoes = models.TextField("Observações", blank=True, null=True)

    criado_por = models.ForeignKey(
        User,
        verbose_name="Criado por",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Admissão"
        verbose_name_plural = "Admissões"

    def __str__(self):
        return f"{self.nome} ({self.codigo})"

    @property
    def supervisor(self):
        return self.criado_por.first_name or self.criado_por.username if self.criado_por else "—"


class Distrato(models.Model):
    nome = models.CharField("Nome do Representante", max_length=150)
    cpf = models.CharField("CPF", max_length=14, blank=True, null=True)
    rg = models.CharField("RG", max_length=20, blank=True, null=True)

    data_admissao = models.DateField("Data de Admissão", null=True, blank=True)
    data_demissao = models.DateField("Data de Demissão", null=True, blank=True)
    dias_trabalhados = models.IntegerField("Dias Trabalhados", null=True, blank=True)
    meses_trabalhados = models.IntegerField("Meses Trabalhados", null=True, blank=True)
    periodo_anos = models.DecimalField("Período em Anos", max_digits=5, decimal_places=2, null=True, blank=True)

    total_geral = models.DecimalField("Total Geral - Comissão período trabalhado",
                                      max_digits=10, decimal_places=2, null=True, blank=True)
    indenizacao_1_12 = models.DecimalField("Indenização 1/12 avos",
                                           max_digits=10, decimal_places=2, null=True, blank=True)
    comissoes_bloqueadas = models.DecimalField("Comissões Bloqueadas",
                                               max_digits=10, decimal_places=2, null=True, blank=True)
    comissao_mes_corrente = models.DecimalField("Comissão do Mês Corrente",
                                                max_digits=10, decimal_places=2, null=True, blank=True)
    gratificacao = models.DecimalField("Gratificação e Outros",
                                       max_digits=10, decimal_places=2, null=True, blank=True)

    total_ultimos_3_meses = models.DecimalField("Total Comissão últimos 3 meses",
                                                max_digits=10, decimal_places=2, null=True, blank=True)
    indenizacao_1_3 = models.DecimalField("Indenização 1/3",
                                          max_digits=10, decimal_places=2, null=True, blank=True)
    bonus = models.DecimalField("Bônus",
                                max_digits=10, decimal_places=2, null=True, blank=True)
    descontos = models.DecimalField("Descontos / Empréstimos / Vales",
                                    max_digits=10, decimal_places=2, null=True, blank=True)
    valor_rescisao = models.DecimalField("Valor da Rescisão",
                                         max_digits=10, decimal_places=2, null=True, blank=True)

    banco = models.CharField("Banco", max_length=50, blank=True, null=True)
    agencia = models.CharField("Agência", max_length=10, validators=[numero_validator], blank=True, null=True)
    operacao = models.CharField("Operação", max_length=5, validators=[numero_validator], blank=True, null=True)
    conta_corrente = models.CharField("Conta Corrente", max_length=15, validators=[numero_validator], blank=True, null=True)
    titular = models.CharField("Titular", max_length=100, blank=True, null=True)
    telefone = models.CharField("Telefone", max_length=15, validators=[numero_validator], blank=True, null=True)

    criado_por = models.ForeignKey(
        User,
        verbose_name="Criado por",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Distrato"
        verbose_name_plural = "Distratos"

    def __str__(self):
        return f"Distrato - {self.nome}"
