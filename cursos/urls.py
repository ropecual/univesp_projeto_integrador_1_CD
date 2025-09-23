# cursos/urls.py

from django.urls import path
from . import views

app_name = 'cursos'
urlpatterns = [
	path('', views.lista_cursos, name='lista_cursos'),
	path('<int:pk>/', views.detalhe_curso, name='detalhe_curso'),
	path('conteudo/<int:pk>/', views.visualizar_conteudo, name='visualizar_conteudo'),

]
