# cursos/views.py

from django.shortcuts import render, get_object_or_404
from .models import Curso, Conteudo
from django.contrib.auth.decorators import login_required
from django.http import Http404

@login_required
def lista_cursos(request):
    cursos = Curso.objects.all()
    return render(request, 'cursos/lista_cursos.html', {'cursos': cursos})


@login_required
def detalhe_curso(request, pk):
    curso = get_object_or_404(request.user.cursos_inscritos, pk=pk)
    return render(request, 'cursos/detalhe_curso.html', {'curso': curso})


@login_required
def visualizar_conteudo(request, pk):
    conteudo = get_object_or_404(Conteudo, pk=pk)
    curso_do_conteudo = conteudo.modulo.curso

    # Verificação de segurança: o aluno tem acesso a este curso?
    if curso_do_conteudo not in request.user.cursos_inscritos.all():
        raise Http404("Você não tem permissão para acessar este conteúdo.")

    return render(request, 'cursos/visualizar_conteudo.html', {'conteudo': conteudo})