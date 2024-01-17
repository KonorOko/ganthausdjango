from rest_framework import serializers
from .models import Vehiculos, Verificaciones, Tenencias, Servicios, NotasVehiculos

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
        

class NotasVehiculosSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotasVehiculos
        fields = ['id', 'nota', 'fecha', 'hora']
        

class DashboardNotificacionesSerializer(serializers.Serializer):
    tenencias_proximas = serializers.ListField()
    verificaciones_proximas = serializers.ListField()
    servicios_proximos = serializers.ListField()