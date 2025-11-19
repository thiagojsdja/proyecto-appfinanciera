from django.contrib import admin
from .models import Cliente, Venta, Pago

# --- CONFIGURACIÓN DE CLIENTES ---
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cedula', 'telefono', 'estado', 'deuda_total_admin')
    search_fields = ('nombre', 'cedula')
    list_filter = ('estado', 'fecha_registro')
    ordering = ('nombre',)
    
    def deuda_total_admin(self, obj):
        # Formato visual simple para la lista
        return f"${obj.calcular_deuda_total():,.0f}".replace(",", ".")
    deuda_total_admin.short_description = "Deuda Actual"

# --- CONFIGURACIÓN AUXILIAR (Pagos dentro de Ventas) ---
class PagoInline(admin.TabularInline):
    model = Pago
    extra = 1
    classes = ('collapse',)
    autocomplete_fields = ['venta']

# --- CONFIGURACIÓN DE VENTAS (Aquí está la magia) ---
@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('producto', 'cliente', 'precio_total_fmt', 'saldo_pendiente_admin', 'estado_calculado')
    search_fields = ('producto', 'cliente__nombre') 
    list_filter = ('pagada', 'fecha_inicio')
    autocomplete_fields = ['cliente'] 
    inlines = [PagoInline] 

    # 1. ORGANIZACIÓN VISUAL DE CAMPOS
    fieldsets = (
        ('Detalles de la Venta', {
            'fields': (('cliente', 'producto'),)
        }),
        ('Cifras (Calculadora Automática)', {
            'description': 'Ingrese el Precio Total y la Cantidad de Cuotas. El monto por cuota se calculará solo.',
            # Agrupamos los campos para que se vean bien
            'fields': (('precio_total', 'cantidad_cuotas'), 'monto_cuota', 'frecuencia_dias')
        }),
        ('Estado', {
            'fields': ('fecha_inicio', 'pagada')
        }),
    )

    # 2. ### CONEXIÓN DEL SCRIPT JAVASCRIPT ###
    # Esto es lo que hace que funcione la automatización
    class Media:
        js = ('gestion/js/admin_ventas.js',)

    # Funciones para mostrar montos bonitos en la lista (con puntos de miles)
    def precio_total_fmt(self, obj):
        return f"{obj.precio_total:,.0f} Gs".replace(",", ".")
    precio_total_fmt.short_description = "Precio Total"

    def saldo_pendiente_admin(self, obj):
        return f"{obj.saldo_pendiente:,.0f} Gs".replace(",", ".")
    saldo_pendiente_admin.short_description = "Saldo Restante"

    def estado_calculado(self, obj):
        return obj.estado_actual
    estado_calculado.short_description = "Estado"

# --- CONFIGURACIÓN DE PAGOS ---
@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('venta', 'monto_fmt', 'fecha_pago', 'metodo')
    list_filter = ('fecha_pago', 'metodo')
    autocomplete_fields = ['venta'] 
    date_hierarchy = 'fecha_pago'

    def monto_fmt(self, obj):
        return f"{obj.monto:,.0f} Gs".replace(",", ".")
    monto_fmt.short_description = "Monto"
