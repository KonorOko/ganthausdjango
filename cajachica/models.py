from django.db import models

class MovimientosCajaChica(models.Model):
    id = models.AutoField(primary_key=True)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    motivo = models.CharField(max_length=300)
    fecha = models.DateField()
    
    def __str__(self) -> str:
        return f'{self.cantidad} - {self.motivo} - {self.fecha}'
    
class NotasCajaChica(models.Model):
    id = models.AutoField(primary_key=True)
    nota = models.CharField(max_length=500)
    fecha = models.DateField(blank=True, null=True)
    hora = models.TimeField(blank=True, null=True)
    
    def __str__(self) -> str:
        return f'{self.nota} - {self.fecha}'