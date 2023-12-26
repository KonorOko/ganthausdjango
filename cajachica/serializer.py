from rest_framework import serializers
from .models import MovimientosCajaChica


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
    cantidad_total = serializers.FloatField()

    class Meta:
        model = MovimientosCajaChica
        exclude = ['id', 'fecha', 'cantidad']
        # 'balance_total', 'balance_gasolina', 'balance_transferencias'
