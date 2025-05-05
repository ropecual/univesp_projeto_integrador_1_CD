from django.http import FileResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Visitante, MaterialPDF, Testemunhos
from .forms import VisitanteForm
from django.shortcuts import redirect
from functools import wraps


def require_session_email(view_func):
	@wraps(view_func)
	def _wrapped_view(request, *args, **kwargs):
		# Verificar se há um email na sessão (indicando um cadastro recente)
		if request.session.get('cadastro_email'):
			return view_func(request, *args, **kwargs)
		else:
			messages.warning(request, "Por favor, preencha o cadastro para acessar os materiais.")
			return redirect('landing_page')

	return _wrapped_view


def landing_page(request):
	if request.method == 'POST':
		form = VisitanteForm(request.POST)
		if form.is_valid():
			visitante = form.save(commit=False)
			# atualizar ou criar visitante
			v, created = Visitante.objects.update_or_create(
				email=visitante.email,
				defaults={
					'nome': visitante.nome,
					'idade': visitante.idade,
					'cidade': visitante.cidade,
					'estado': visitante.estado,
					'ultima_visita': visitante.ultima_visita,
				}
			)
			if created:
				messages.success(request, "Registro realizado com sucesso!")
			else:
				messages.success(request, "Bem-vindo de volta!")

			# guardar email na sessão e redirecionar para download
			request.session['cadastro_email'] = v.email
			# supondo que queira o primeiro PDF ativo:
			primeiro_pdf = MaterialPDF.objects.filter(ativo=True).first()
			if primeiro_pdf:
				return redirect('download_pdf', pk=primeiro_pdf.pk)
			else:
				messages.warning(request, "Nenhum material disponível.")
				return redirect('landing_page')

	else:
		form = VisitanteForm()

	testemunhos = Testemunhos.objects.all()
	return render(request, 'main/landing_page.html', {
		'form': form,
		'testemunhos': testemunhos,
	})


@require_session_email
def download_pdf(request, pk):
	pdf = get_object_or_404(MaterialPDF, pk=pk, ativo=True)

	try:
		return FileResponse(pdf.arquivo.open('rb'),
							as_attachment=True,
							filename=pdf.arquivo.name)
	except IOError:
		raise Http404("Arquivo não encontrado")


def obrigado(request):
	return render(request, 'main/obrigado.html')
