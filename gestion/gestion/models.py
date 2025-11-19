from django.db import models
from django.utils import timezone
from datetime import timedelta
import os
from django.conf import settings

class Cliente(models.Model):
    ESTADOS = [
        ('ACTIVO', 'Activo'),
        ('COMPLETADO', 'Completado'),
        ('ATRASADO', 'Atrasado'),
    ]
    
    nombre = models.CharField(max_length=100)
    cedula = models.CharField(max_length=20, unique=True, verbose_name="Cédula/DNI")
    telefono = models.CharField(max_length=20)
    direccion = models.TextField(blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='ACTIVO')
    
    # IA / Lógica Predictiva Simple
    score_crediticio = models.IntegerField(default=100, help_text="Puntaje calculado por el sistema (0-100)")

    def __str__(self):
        return f"{self.nombre} ({self.cedula})"

    def calcular_deuda_total(self):
        total = 0
        for venta in self.ventas.all():
            total += venta.saldo_pendiente
        return total

class Venta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='ventas')
    producto = models.CharField(max_length=200)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad_cuotas = models.IntegerField()
    monto_cuota = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_inicio = models.DateField(default=timezone.now)
    # Frecuencia de pago (días)
    frecuencia_dias = models.IntegerField(default=30, verbose_name="Frecuencia (días)")
    
    pagada = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.producto} - {self.cliente.nombre}"

    @property
    def total_pagado(self):
        return sum(pago.monto for pago in self.pagos.all())

    @property
    def saldo_pendiente(self):
        return self.precio_total - self.total_pagado

    @property
    def cuotas_pagadas_count(self):
        # Aproximación basada en monto
        if self.monto_cuota > 0:
            return int(self.total_pagado // self.monto_cuota)
        return 0

    @property
    def proximo_vencimiento(self):
        # Calcula la fecha de la siguiente cuota impaga
        cuotas_pagadas = self.cuotas_pagadas_count
        if cuotas_pagadas >= self.cantidad_cuotas:
            return None # Terminó de pagar
        
        dias_a_sumar = (cuotas_pagadas + 1) * self.frecuencia_dias
        fecha = self.fecha_inicio + timedelta(days=dias_a_sumar)
        return fecha

    @property
    def estado_actual(self):
        if self.saldo_pendiente <= 0:
            return "COMPLETADO"
        
        vencimiento = self.proximo_vencimiento
        if vencimiento and vencimiento < timezone.now().date():
            return "ATRASADO"
        
        if vencimiento and vencimiento <= (timezone.now().date() + timedelta(days=3)):
            return "PROXIMO_VENCER"
            
        return "AL_DIA"

class Pago(models.Model):
    METODOS = [
        ('EFECTIVO', 'Efectivo'),
        ('TRANSFERENCIA', 'Transferencia'),
        ('OTRO', 'Otro'),
    ]
    
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='pagos')
    fecha_pago = models.DateField(default=timezone.now)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    nota = models.CharField(max_length=200, blank=True)
    metodo = models.CharField(max_length=20, choices=METODOS, default='EFECTIVO')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Actualizar estado del cliente tras el pago
        if self.venta.saldo_pendiente <= 0:
            self.venta.pagada = True
            self.venta.save()