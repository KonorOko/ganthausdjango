from django.db import models

class Vehiculos(models.Model):
    id = models.IntegerField(primary_key=True)
    modelo = models.CharField(max_length=100, null=True, blank=True)
    año = models.IntegerField(null=True, blank=True)
    placa = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self) -> str:
        return f'{self.id} - {self.modelo} - {self.año} - {self.placa}'
    
class Verificaciones(models.Model):
    vehiculo = models.ForeignKey(Vehiculos, on_delete=models.CASCADE)
    fecha = models.DateField()
    
    def __str__(self) -> str:
        return f'{self.vehiculo} - {self.fecha}'
    