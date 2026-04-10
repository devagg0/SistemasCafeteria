from django.urls import path
from .views.auth import login_view, home_view, logout_view
from .views.clientes import registrar_cliente, listar_clientes, obtener_cliente, actualizar_cliente, eliminar_cliente

urlpatterns = [
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('clientes/', listar_clientes, name='listar_clientes'),
    path('clientes/registrar/', registrar_cliente, name='registrar_cliente'),
    path('clientes/<str:cod_cliente>/', obtener_cliente, name='obtener_cliente'),
    path('clientes/<str:cod_cliente>/actualizar/', actualizar_cliente, name='actualizar_cliente'),
    path('clientes/<str:cod_cliente>/eliminar/', eliminar_cliente, name='eliminar_cliente'),
]