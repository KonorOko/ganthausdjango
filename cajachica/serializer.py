from rest_framework import serializers
from .models import MovimientosCajaChica, NotasCajaChica


class MovimientosCajaChicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovimientosCajaChica
        fields = '__all__'


class MovimientosBalanceSerializer(serializers.ModelSerializer):
    cantidad = serializers.FloatField()

    class Meta:
        model = MovimientosCajaChica
        exclude = ['motivo', 'id']


class BalanceTotalSerializer(serializers.ModelSerializer):
    cantidad = serializers.StringRelatedField()
    movimientos = serializers.IntegerField()

    class Meta:
        model = MovimientosCajaChica
        exclude = ['motivo', 'id', 'fecha']


class MovimientosDataSerializer(serializers.ModelSerializer):
    cantidad = serializers.FloatField()

    class Meta:
        model = MovimientosCajaChica
        exclude = ['id', 'fecha']


class AnaliticsDataSerializer(serializers.ModelSerializer):
    motivo = serializers.CharField()
    cantidad_total = serializers.StringRelatedField()

    class Meta:
        model = MovimientosCajaChica
        exclude = ['id', 'fecha', 'cantidad']
        
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
    
    
class NotasCajaChicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotasCajaChica
        fields = ['id', 'nota', 'fecha', 'hora']
        