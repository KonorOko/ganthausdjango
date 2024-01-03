from rest_framework import viewsets
from .serializer import VehiculosSerializer, VerificacionesSerializer, FirstVerificacionesSerializer, TenenciasSerializer
from .models import Vehiculos, Verificaciones

# Create your views here.
class VehiculosView(viewsets.ModelViewSet):
    serializer_class = VehiculosSerializer
    queryset = Vehiculos.objects.all()
    
class VerificacionesView(viewsets.ModelViewSet):
    serializer_class = VerificacionesSerializer
    queryset = Verificaciones.objects.all()
    
class FirstVerificacionesView(viewsets.ModelViewSet):
    serializer_class = FirstVerificacionesSerializer
    
    def get_queryset(self):
        if Verificaciones.objects.count() == 0:
            return []
        else:
            queryset = Verificaciones.objects.all().order_by('fecha')[:3]
            return queryset
        
class TenenciasView(viewsets.ModelViewSet):
    serializer_class = TenenciasSerializer
    queryset = Verificaciones.objects.all()