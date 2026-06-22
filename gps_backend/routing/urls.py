from django.urls import path
from . import views

urlpatterns = [
    path('api/route/', views.route_api, name='route_api'),
    path('api/zonas-rojas/', views.zonas_rojas_api, name='zonas_rojas'),
    path('api/casetas/', views.listar_casetas, name='listar_casetas'),
    path('api/casetas/cercanas/', views.casetas_cercanas, name='casetas_cercanas'),
]