from django.contrib import admin

from django.contrib import admin
from .models import Visitante, MaterialPDF, Testemunhos


@admin.register(Visitante)
class VisitanteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'cidade', 'estado', 'primeira_visita', 'ultima_visita')
    search_fields = ('nome', 'email')
    list_filter = ('cidade', 'estado', 'primeira_visita')

@admin.register(MaterialPDF)
class MaterialPDFAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'data_upload', 'ativo')
    list_filter = ('ativo',)
    search_fields = ('titulo', 'descricao')


@admin.register(Testemunhos)
class TestemunhosAdmin(admin.ModelAdmin):
    list_display = ('nome', 'texto_sobre', 'descricao')
    search_fields = ('nome', 'texto_sobre', 'descricao')