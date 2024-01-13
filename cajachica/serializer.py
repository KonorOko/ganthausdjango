from rest_framework import serializers
from .models import MovimientosCajaChica, NotasCajaChica


class MovimientosCajaChicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovimientosCajaChica
        fields = '__all__'
        
class CajaChicaPageSerializer2(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = MovimientosCajaChica
        fields = ['id', 'cantidad', 'motivo', 'fecha']   
        

class CajaChicaPageSerializer(serializers.Serializer):
    datos = CajaChicaPageSerializer2(many=True)
    balance_total = serializers.FloatField()
    balance_diario = serializers.FloatField()
    registros_diarios = serializers.IntegerField()
    crecimiento_mensual = serializers.FloatField()
    
class CajaChicaAnalisisSerializer2(serializers.ModelSerializer):
    mes_nombre = serializers.CharField()
    class Meta:
        model = MovimientosCajaChica
        fields = ['cantidad', 'mes_nombre'] 
        
        
class CajaChicaAnalisisSerializer(serializers.Serializer):
    # balance agrupados por mese
    balance_anual_agrupado = serializers.ListField()
    
    # datos sobre el balance de la caja chica
    balance_total = serializers.FloatField()
    balance_anual = serializers.FloatField()
    balance_mensual = serializers.FloatField()
    balance_diario = serializers.FloatField()
    registros_anuales = serializers.IntegerField()
    registros_mensuales = serializers.IntegerField()
    registros_diarios = serializers.IntegerField()
    crecimiento_mensual = serializers.FloatField()
    
class CajaChicaAnalisisSerializerMid(serializers.Serializer):
    comparativa_mensual = serializers.ListField()
    tipos_de_egresos = serializers.ListField()
    
class CajaChicaAnalisisVehiculosSerializer(serializers.Serializer):
    consumo_gasolina_mensual = serializers.FloatField()
    vehiculos_mayor_consumo_4_meses = serializers.ListField()
    datos_ultimos_4_meses = serializers.ListField()
    consumo_anual = serializers.ListField()
    
    
class NotasCajaChicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotasCajaChica
        fields = ['id', 'nota', 'fecha', 'hora']
        