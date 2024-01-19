from rest_framework import serializers
from .models import Ventas


class VentasSerializer(serializers.ModelSerializer):
    distribucion = serializers.FloatField()
    class Meta:
        model = Ventas
        fields = '__all__'


class VentasPageSerializerID(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = Ventas
        fields = "__all__"


class VentasPageSerializer(serializers.Serializer):
    data = VentasPageSerializerID(many=True)
    monthly_sales = serializers.FloatField()