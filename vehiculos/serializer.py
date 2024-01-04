from rest_framework import serializers
from .models import Vehiculos, Verificaciones, Tenencias

class VehiculosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehiculos
        fields = '__all__'
        
class VerificacionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verificaciones
        fields = ('id', 'vehiculo', 'fecha')
        
class FirstVerificacionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verificaciones
        fields = ('vehiculo', 'fecha')
        
    def get_queryset(self):
        if Verificaciones.objects.count() == 0:
            return []
        else:
            queryset = Verificaciones.objects.all().order_by('-fecha')[:3]
            return queryset
        
class TenenciasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenencias
        fields = ('id', 'vehiculo', 'fecha')
        