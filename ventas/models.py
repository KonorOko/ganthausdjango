from django.db import models
from django.utils import timezone

class Ventas(models.Model):
    factura = models.CharField(max_length=50)
    fecha = models.DateField(default=timezone.now)
    cliente = models.CharField(max_length=50)
    vendedor = models.CharField(max_length=50)
    distribucion = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    pagado = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_pago = models.DateField(default=timezone.now, blank=True, null=True)
    saldo_pendiente = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        self.saldo_pendiente = (self.total - self.pagado)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.fecha} Factura: {self.factura}"