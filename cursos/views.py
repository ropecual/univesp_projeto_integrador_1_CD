# cursos/views.py
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .models import Curso, Conteudo
from django.contrib.auth.decorators import login_required
from django.http import Http404


@login_required
def inscrever_curso(request, pk):
	curso = get_object_or_404(Curso, pk=pk)
	# Adiciona o aluno atual à lista de alunos do curso
	curso.alunos.add(request.user)
	messages.success(request, f'Inscrição no curso "{curso.titulo}" realizada com sucesso!')
	return redirect('cursos:detalhe_curso', pk=curso.pk)


@login_required
def desinscrever_curso(request, pk):
	curso = get_object_or_404(Curso, pk=pk)

	# Remove o aluno atual da lista de alunos do curso
	curso.alunos.remove(request.user)

	messages.success(request, f'Sua inscrição no curso "{curso.titulo}" foi cancelada.')

	# Redireciona de volta para a lista de cursos disponíveis
	return redirect('cursos:lista_cursos')


@login_required
def lista_cursos(request):
	# Pega os IDs dos cursos em que o aluno já está matriculado
	cursos_matriculados_ids = request.user.cursos_inscritos.values_list('id', flat=True)

	# Busca os cursos disponíveis (todos, exceto os que ele já se matriculou)
	cursos_disponiveis = Curso.objects.exclude(id__in=cursos_matriculados_ids)

	context = {
		'cursos_disponiveis': cursos_disponiveis,
	}
	return render(request, 'cursos/lista_cursos.html', context)


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
