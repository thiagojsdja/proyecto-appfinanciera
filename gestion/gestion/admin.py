from django.contrib import admin
from django.contrib.humanize.templatetags.humanize import intcomma
from .models import Cliente, Venta, Pago

# --- CONFIGURACIÓN DE CLIENTES ---
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cedula', 'telefono', 'estado_visual', 'deuda_visual')
    search_fields = ('nombre', 'cedula')
    list_filter = ('estado', 'fecha_registro')
    ordering = ('nombre',)
    list_per_page = 20

    # Formato visual para la deuda (4.200.000 Gs.)
    def deuda_visual(self, obj):
        deuda = obj.calcular_deuda_total()
        return f"{intcomma(int(deuda)).replace(',', '.')} Gs."
    deuda_visual.short_description = "Deuda Total"
    
    # Para que se pueda ordenar por deuda (aunque es un cálculo)
    # deuda_visual.admin_order_field = 'ventas__precio_total' 

    def estado_visual(self, obj):
        return obj.estado
    estado_visual.short_description = "Estado"

# --- CONFIGURACIÓN AUXILIAR (Pagos dentro de Ventas) ---
class PagoInline(admin.TabularInline):
    model = Pago
    extra = 0  # No mostrar filas vacías por defecto
    classes = ('collapse',)
    autocomplete_fields = ['venta']
    verbose_name = "Pago Realizado"
    verbose_name_plural = "Historial de Pagos en esta Venta"

# --- CONFIGURACIÓN DE VENTAS ---
@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('producto', 'cliente', 'precio_visual', 'saldo_visual', 'estado_calculado')
    search_fields = ('producto', 'cliente__nombre') 
    list_filter = ('pagada', 'fecha_inicio')
    autocomplete_fields = ['cliente'] 
    inlines = [PagoInline] 

    # Organización visual del formulario
    fieldsets = (
        ('📦 Detalles de la Venta', {
            'fields': (('cliente', 'producto'),)
        }),
        ('💰 Cifras (Calculadora Automática)', {
            'description': 'Ingrese el Precio Total y la Cantidad de Cuotas. El monto por cuota se calculará solo.',
            'fields': (('precio_total', 'cantidad_cuotas'), 'monto_cuota', 'frecuencia_dias')
        }),
        ('📅 Fechas y Estado', {
            'fields': ('fecha_inicio', 'pagada')
        }),
    )

    # Conexión del Script de Automatización
    class Media:
        js = ('gestion/js/admin_ventas.js',)

    # Funciones visuales para la lista
    def precio_visual(self, obj):
        return f"{intcomma(int(obj.precio_total)).replace(',', '.')} Gs."
    precio_visual.short_description = "Precio Total"

    def saldo_visual(self, obj):
        return f"{intcomma(int(obj.saldo_pendiente)).replace(',', '.')} Gs."
    saldo_visual.short_description = "Saldo Restante"

    def estado_calculado(self, obj):
        return obj.estado_actual
    estado_calculado.short_description = "Estado"

# --- CONFIGURACIÓN DE PAGOS ---
@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('venta', 'monto_visual', 'fecha_pago', 'metodo')
    list_filter = ('fecha_pago', 'metodo')
    search_fields = ('venta__producto', 'venta__cliente__nombre')
    autocomplete_fields = ['venta'] 
    date_hierarchy = 'fecha_pago'

    def monto_visual(self, obj):
        return f"{intcomma(int(obj.monto)).replace(',', '.')} Gs."
    monto_visual.short_description = "Monto Pagado"
