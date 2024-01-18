from django.db import models

# Create your models here.
class Ventas(models.Model):
    id = models.IntegerField(primary_key=True)
    serie = models.CharField(max_length=50)
    fecha = models.DateField()
    cliente = models.CharField(max_length=50)
    vendedor = models.CharField(max_length=50)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    distribucion = models.DecimalField(max_digits=10, decimal_places=2)
    pagado = models.DecimalField(max_digits=10, decimal_places=2)
    saldo_pendiente = models.DecimalField(max_digits=10, decimal_places=2)
    
    def save(self, *args, **kwargs):
        self.saldo_pendiente = (self.total - self.pagado)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.serie