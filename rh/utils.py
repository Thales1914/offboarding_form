import openpyxl
from django.http import HttpResponse
from .models import Desligamento
from io import BytesIO

def exportar_ficha_excel(desligamento_id):
    desligamento = Desligamento.objects.get(pk=desligamento_id)

    wb = openpyxl.load_workbook("FORMULÁRIO DESLIGAMENTO RCA.xlsx")
    ws = wb.active

    ws["B3"] = desligamento.supervisor
    ws["E3"] = desligamento.demissao.strftime("%d/%m/%Y") if desligamento.demissao else ""
    ws["F2"] = desligamento.admissao.strftime("%d/%m/%Y") if desligamento.admissao else ""

    ws["A6"] = desligamento.codigo
    ws["B6"] = desligamento.nome
    ws["C6"] = desligamento.contato
    ws["D6"] = desligamento.admissao.strftime("%d/%m/%Y") if desligamento.admissao else ""
    ws["E6"] = desligamento.demissao.strftime("%d/%m/%Y") if desligamento.demissao else ""
    ws["F6"] = desligamento.area_atuacao

    ws["C7"] = desligamento.motivo or ""

    itens = [
        desligamento.fardamento,
        desligamento.chip_voz,
        desligamento.chip_dados,
        desligamento.tablet,
        desligamento.carregador_tablet,
        desligamento.fone_tablet,
        desligamento.catalogo,
        desligamento.bloco_pedido,
        desligamento.carta_pedido_demissao,
        desligamento.relatorio_inadimplencia,
    ]
    for idx, valor in enumerate(itens, start=10):
        ws[f"A{idx}"] = "✅" if valor else "❌"

    ws["E22"] = "Sim" if desligamento.substituto else "Não"
    ws["E23"] = "Sim" if desligamento.telemarketing else "Não"
    ws["E24"] = "Sim" if desligamento.nova_contratacao else "Não"

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    response = HttpResponse(
        output,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = f'attachment; filename="ficha_{desligamento.codigo}.xlsx"'
    return response
