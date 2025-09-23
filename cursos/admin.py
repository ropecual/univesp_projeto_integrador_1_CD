from django.contrib import admin

from .models import Curso, Modulo, Conteudo

class CursoAdmin(admin.ModelAdmin):
    # Isso cria uma caixa de seleção dupla, muito mais fácil de usar
    filter_horizontal = ('alunos',)

# Substitua a linha antiga pelo bloco abaixo
admin.site.register(Curso, CursoAdmin)
admin.site.register(Modulo)
admin.site.register(Conteudo)