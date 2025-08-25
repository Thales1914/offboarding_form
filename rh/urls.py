from django.urls import path
from . import views

urlpatterns = [
    path(
        "exportar-excel/<int:pk>/",
        views.exportar_excel_individual,
        name="exportar_excel_individual",
    ),
]
