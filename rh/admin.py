from django.contrib import admin
from django.urls import path, reverse
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.utils.html import format_html
from django.db.models import Count
from openpyxl import load_workbook
import os

from .models import Desligamento


class FiltroQtdDesligamentos(admin.SimpleListFilter):
    title = "Quantidade de desligamentos"
    parameter_name = "qtd_desligamentos"

    def lookups(self, request, model_admin):
        return [
            ("1", "1 desligamento"),
            ("5", "5 ou mais"),
            ("10", "10 ou mais"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "1":
            return queryset.annotate(total=Count("criado_por")).filter(total=1)
        if self.value() == "5":
            return queryset.annotate(total=Count("criado_por")).filter(total__gte=5)
        if self.value() == "10":
            return queryset.annotate(total=Count("criado_por")).filter(total__gte=10)
        return queryset


@admin.register(Desligamento)
class DesligamentoAdmin(admin.ModelAdmin):
    list_display = (
        "nome",
        "codigo",
        "supervisor",
        "demissao",
        "area_atuacao",
        "criado_por",
        "qtd_desligamentos_colaborador",
    )
    search_fields = ("nome", "codigo", "area_atuacao")
    list_filter = ("area_atuacao", "demissao", "criado_por", FiltroQtdDesligamentos)

    fieldsets = (
        ('📌 Dados do Colaborador', {
            'fields': ('codigo', 'nome', 'contato', 'admissao', 'demissao', 'area_atuacao')
        }),
        ('📄 Motivo do desligamento', {
            'fields': ('motivo',)
        }),
        ('📦 Itens a devolver', {
            'fields': (
                'fardamento', 'chip_voz', 'chip_dados', 'tablet',
                'carregador_tablet', 'fone_tablet', 'catalogo',
                'bloco_pedido', 'carta_pedido_demissao', 'relatorio_inadimplencia'
            )
        }),
        ('🔎 Perguntas extras', {
            'fields': ('substituto', 'telemarketing', 'nova_contratacao')
        }),
        ('📝 Observações', {
            'fields': ('observacoes',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not obj.pk: 
            obj.criado_por = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate(total_desligamentos=Count("criado_por"))
        if request.user.is_superuser or request.user.groups.filter(name="RH").exists():
            return qs
        return qs.filter(criado_por=request.user)

    def qtd_desligamentos_colaborador(self, obj):
        return Desligamento.objects.filter(criado_por=obj.criado_por).count()
    qtd_desligamentos_colaborador.short_description = "Qtd desligamentos"

    def has_export_permission(self, request):
        return request.user.is_superuser or request.user.groups.filter(name="RH").exists()

    def has_view_permission(self, request, obj=None):
        if obj is None:
            return True
        if request.user.is_superuser or request.user.groups.filter(name="RH").exists():
            return True
        return obj.criado_por == request.user

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:desligamento_id>/exportar_excel/',
                self.admin_site.admin_view(self.exportar_excel),
                name="rh_desligamento_exportar_excel_individual",
            ),
        ]
        return custom_urls + urls

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        if request.user.is_superuser or request.user.groups.filter(name="RH").exists():
            export_url = reverse("admin:rh_desligamento_exportar_excel_individual", args=[object_id])
            extra_context['extra_buttons'] = format_html(
                f'<a class="button" style="margin-left:10px;" href="{export_url}">📤 Exportar Excel</a>'
            )
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def exportar_excel(self, request, desligamento_id):
        if not self.has_export_permission(request):
            raise PermissionDenied("Você não tem permissão para exportar este registro.")

        desligamento = Desligamento.objects.get(id=desligamento_id)

        modelo_path = os.path.join(os.path.dirname(__file__), "FORMULÁRIO DESLIGAMENTO RCA.xlsx")
        wb = load_workbook(modelo_path)
        ws = wb.active

        ws["B3"] = desligamento.supervisor or ""
        ws["E3"] = desligamento.demissao.strftime("%d/%m/%Y") if desligamento.demissao else ""
        ws["F2"] = desligamento.admissao.strftime("%d/%m/%Y") if desligamento.admissao else ""

        ws["A6"] = desligamento.codigo or ""
        ws["B6"] = desligamento.nome or ""
        ws["C6"] = desligamento.contato or ""
        ws["D6"] = desligamento.admissao.strftime("%d/%m/%Y") if desligamento.admissao else ""
        ws["E6"] = desligamento.demissao.strftime("%d/%m/%Y") if desligamento.demissao else ""
        ws["F6"] = desligamento.area_atuacao or ""

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
        for i, valor in enumerate(itens, start=10):
            ws[f"A{i}"] = "SIM" if valor else "NÃO"

        ws["E22"] = "SIM" if desligamento.substituto else "NÃO"
        ws["E23"] = "SIM" if desligamento.telemarketing else "NÃO"
        ws["E24"] = "SIM" if desligamento.nova_contratacao else "NÃO"

        ws["C26"] = desligamento.observacoes or ""

        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = f'attachment; filename="desligamento_{desligamento.codigo}.xlsx"'
        wb.save(response)
        return response
