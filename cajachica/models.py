from django.db import models

class MovimientosCajaChica(models.Model):
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    motivo = models.CharField(max_length=100)
    fecha = models.DateField()
    
    def __str__(self) -> str:
        return f'{self.cantidad} - {self.motivo} - {self.fecha}'