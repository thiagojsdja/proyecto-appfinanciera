from django.contrib import admin
from django.urls import path
from gestion import views

urlpatterns = [
    # Panel de administrador
    path('admin/', admin.site.urls),
    
    # Login personalizado (usando el de admin)
    path('accounts/login/', admin.site.login, name='login'),
    
    # --- API INTERNA (Este es el código nuevo del Paso 2) ---
    # Esta ruta permite que el Javascript pregunte el monto de una venta
    path('api/venta/<int:venta_id>/', views.obtener_detalle_venta, name='api_venta_detalle'),
    
    # Rutas de tu aplicación (Dashboard, Clientes, Perfil)
    path('', views.dashboard, name='dashboard'),
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('cliente/<int:cliente_id>/', views.perfil_cliente, name='perfil_cliente'),
]