from rest_framework import serializers
from .models import Ventas


class VentasSerializer(serializers.ModelSerializer):
    distribucion = serializers.FloatField()
    class Meta:
        model = Ventas
        fields = '__all__'
