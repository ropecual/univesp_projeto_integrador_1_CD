from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('materiais/', views.materiais, name='materiais'),
    path('obrigado/', views.obrigado, name='obrigado'),
]