from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
	path('', views.landing_page, name='landing_page'),
	path('download/<int:pk>/', views.download_pdf, name='download_pdf'),

	path('login/', auth_views.LoginView.as_view(template_name='cursos/login.html'), name='login'),
	path('logout/', auth_views.LogoutView.as_view(next_page='landing_page'), name='logout'),
]
