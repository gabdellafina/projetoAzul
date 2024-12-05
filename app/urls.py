from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('perfil/', views.perfil, name='perfil'),
    path('locais/', views.locais, name='locais'),
    path('marcar_consulta/', views.marcar_consulta, name='marcar_consulta'),
    path('consultar_exames/', views.consultar_exames, name='consultar_exames'),
    path('consultar_calendario/', views.consultar_calendario, name='consultar_calendario'),
    path('carteira_vacinacao/', views.carteira_vacinacao, name='carteira_vacinacao'),
    path('eventos_saude/', views.eventos_saude, name='eventos_saude'),
]