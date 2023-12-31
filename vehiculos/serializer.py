from rest_framework import serializers
from .models import Vehiculos, Verificaciones, Tenencias, Servicios

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

class TenenciasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenencias
        fields = ('id', 'vehiculo', 'fecha')
        
class ServiciosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicios
        fields = ('id', 'vehiculo', 'fecha')
        