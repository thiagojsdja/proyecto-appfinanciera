from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta
from .models import Cliente, Venta, Pago
import json

# --- UTILS IA / PREDICCIÓN ---
def sugerir_mensaje_cobro(cliente, dias_atraso):
    """Genera un mensaje de WhatsApp basado en el nivel de atraso (IA Simbólica)"""
    if dias_atraso < 0:
        return f"Hola {cliente.nombre}, recordatorio amable de tu cuota próxima a vencer."
    elif dias_atraso <= 5:
        return f"Hola {cliente.nombre}, notamos un pequeño atraso en tu cuota. ¿Todo bien?"
    else:
        return f"Estimado {cliente.nombre}, necesitamos regularizar su deuda pendiente de inmediato."

# --- VISTAS ---

@login_required
def dashboard(request):
    hoy = timezone.now().date()
    
    # Estadísticas Generales
    total_clientes = Cliente.objects.count()
    total_prestado = Venta.objects.aggregate(Sum('precio_total'))['precio_total__sum'] or 0
    total_cobrado = Pago.objects.aggregate(Sum('monto'))['monto__sum'] or 0
    total_pendiente = total_prestado - total_cobrado
    
    # Filtros de Estado
    ventas_activas = Venta.objects.filter(pagada=False)
    clientes_atrasados = 0
    proximos_pagos = []
    
    for venta in ventas_activas:
        estado = venta.estado_actual
        if estado == "ATRASADO":
            clientes_atrasados += 1
        elif estado == "PROXIMO_VENCER":
            proximos_pagos.append({
                'cliente': venta.cliente.nombre,
                'monto': venta.monto_cuota,
                'fecha': venta.proximo_vencimiento
            })

    # Datos para Gráficos (Chart.js)
    # 1. Cobros últimos 6 meses (simplificado)
    labels_meses = []
    data_cobros = []
    for i in range(5, -1, -1):
        mes = hoy - timedelta(days=i*30)
        pagos_mes = Pago.objects.filter(fecha_pago__year=mes.year, fecha_pago__month=mes.month).aggregate(Sum('monto'))['monto__sum'] or 0
        labels_meses.append(mes.strftime('%b'))
        data_cobros.append(float(pagos_mes))

    context = {
        'total_clientes': total_clientes,
        'total_pendiente': total_pendiente,
        'total_cobrado': total_cobrado,
        'clientes_atrasados': clientes_atrasados,
        'proximos_pagos': proximos_pagos,
        'chart_labels': json.dumps(labels_meses),
        'chart_data': json.dumps(data_cobros),
        'tasa_morosidad': round((clientes_atrasados / total_clientes * 100), 1) if total_clientes > 0 else 0
    }
    return render(request, 'dashboard.html', context)

@login_required
def lista_clientes(request):
    query = request.GET.get('q')
    filtro = request.GET.get('filtro')
    
    clientes = Cliente.objects.all().order_by('-fecha_registro')
    
    if query:
        clientes = clientes.filter(
            Q(nombre__icontains=query) | 
            Q(cedula__icontains=query)
        )
        
    context = {'clientes': clientes}
    return render(request, 'lista_clientes.html', context)

@login_required
def perfil_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    ventas = cliente.ventas.all()
    
    # Generar sugerencia de IA
    mensaje_sugerido = ""
    tiene_atraso = False
    for v in ventas:
        if v.estado_actual == "ATRASADO":
            tiene_atraso = True
            break
    
    mensaje_sugerido = sugerir_mensaje_cobro(cliente, 10 if tiene_atraso else -1)
            
    return render(request, 'perfil_cliente.html', {
        'cliente': cliente, 
        'ventas': ventas,
        'mensaje_ia': mensaje_sugerido
    })
# ... (todo tu código anterior) ...

from django.http import JsonResponse

# Función para obtener la cuota automáticamente
def obtener_detalle_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    return JsonResponse({'monto_cuota': venta.monto_cuota})