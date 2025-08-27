from django import forms
from .models import Distrato


class DistratoForm(forms.ModelForm):
    class Meta:
        model = Distrato
        fields = "__all__"
        widgets = {
            "banco": forms.TextInput(attrs={
                "placeholder": "Ex: Caixa Econômica",
                "maxlength": "50"
            }),
            "agencia": forms.TextInput(attrs={
                "placeholder": "Somente números",
                "maxlength": "10"
            }),
            "operacao": forms.TextInput(attrs={
                "placeholder": "Ex: 001",
                "maxlength": "5"
            }),
            "conta_corrente": forms.TextInput(attrs={
                "placeholder": "Conta sem dígito",
                "maxlength": "15"
            }),
            "titular": forms.TextInput(attrs={
                "placeholder": "Nome completo do titular",
                "maxlength": "100"
            }),
            "telefone": forms.TextInput(attrs={
                "placeholder": "(99) 99999-9999",
                "maxlength": "15"
            }),
        }
