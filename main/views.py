from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Visitante, MaterialPDF
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
      # Verificar se já existe um visitante com este email
      try:
        v_existente = Visitante.objects.get(email=visitante.email)
        v_existente.ultima_visita = visitante.ultima_visita
        v_existente.save()
        messages.success(request, "Bem-vindo de volta!")
      except Visitante.DoesNotExist:
        visitante.save()
        messages.success(request, "Registro realizado com sucesso!")

      # Redirecionar para a página de materiais
      return redirect('materiais')
  else:
    form = VisitanteForm()

  return render(request, 'main/landing_page.html', {
    'form': form,
  })

@require_session_email
def materiais(request):
  pdfs_ativos = MaterialPDF.objects.filter(ativo=True)
  return render(request, 'main/materiais.html', {
    'pdfs': pdfs_ativos,
  })


def obrigado(request):
  return render(request, 'main/obrigado.html')