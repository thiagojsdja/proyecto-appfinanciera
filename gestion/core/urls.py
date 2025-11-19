from django.contrib import admin
from django.urls import path
from gestion import views

urlpatterns = [
    # Panel de administrador
    path('admin/', admin.site.urls),
    
    # --- ESTA ES LA LÍNEA CLAVE PARA EL LOGIN ---
    path('accounts/login/', admin.site.login, name='login'),
    
    # Rutas de tu aplicación
    path('', views.dashboard, name='dashboard'),
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('cliente/<int:cliente_id>/', views.perfil_cliente, name='perfil_cliente'),
]