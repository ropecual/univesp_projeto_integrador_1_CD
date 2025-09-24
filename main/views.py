# main/views.py

from django.http import FileResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Visitante, MaterialPDF, Testemunhos
from .forms import VisitanteForm, RegistrationForm
from django.contrib.auth.models import User
from django.contrib.auth import login


def landing_page(request):
	# Instancia os dois formulários para serem exibidos na página
	registration_form = RegistrationForm()
	ebook_form = VisitanteForm()

	if request.method == 'POST':
		# Identifica qual formulário foi enviado através de um campo oculto
		form_type = request.POST.get('form_type')

		# Lógica para o formulário de CADASTRO DE ALUNO
		if form_type == 'register':
			registration_form = RegistrationForm(request.POST)
			if registration_form.is_valid():
				user = registration_form.save(commit=False)
				user.username = registration_form.cleaned_data['email']  # Define o username como o e-mail
				user.set_password(registration_form.cleaned_data['password'])
				user.save()

				# Loga o usuário automaticamente após o cadastro
				login(request, user, backend='core.backends.EmailBackend')
				messages.success(request, "Cadastro realizado com sucesso! Bem-vindo(a)!")
				return redirect('cursos:lista_cursos')  # Redireciona para a área de cursos

		# Lógica para o formulário de DOWNLOAD DO E-BOOK
		elif form_type == 'ebook':
			ebook_form = VisitanteForm(request.POST)
			if ebook_form.is_valid():
				visitante_data = ebook_form.cleaned_data
				# Salva ou atualiza o visitante (lead)
				Visitante.objects.update_or_create(
					email=visitante_data['email'],
					defaults={'nome': visitante_data['nome']}
				)
				messages.success(request, 'Obrigado! Seu e-book está pronto para download.')

				primeiro_pdf = MaterialPDF.objects.filter(ativo=True).first()
				if primeiro_pdf:
					return redirect('download_pdf', pk=primeiro_pdf.pk)
				else:
					messages.warning(request, "Nenhum e-book disponível no momento.")

	# Busca os depoimentos para exibir na página
	testemunhos = Testemunhos.objects.all()

	# Envia ambos os formulários e os depoimentos para o template
	context = {
		'registration_form': registration_form,
		'ebook_form': ebook_form,
		'testemunhos': testemunhos,
	}
	return render(request, 'main/landing_page.html', context)


def download_pdf(request, pk):
	"""
	Força o download do arquivo PDF.
	"""
	pdf = get_object_or_404(MaterialPDF, pk=pk, ativo=True)
	try:
		return FileResponse(pdf.arquivo.open('rb'), as_attachment=True, filename=pdf.arquivo.name)
	except IOError:
		raise Http404("Arquivo não encontrado")


