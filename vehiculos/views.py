from rest_framework import viewsets
from .serializer import VehiculosSerializer, VerificacionesSerializer, FirstVerificacionesSerializer, TenenciasSerializer, ServiciosSerializer
from .models import Vehiculos, Verificaciones, Tenencias, Servicios

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
    queryset = Tenencias.objects.all()
    

class FirstTenenciasView(viewsets.ModelViewSet):
    serializer_class = TenenciasSerializer
    
    def get_queryset(self):
        if Tenencias.objects.count() == 0:
            return []
        else:
            queryset = Tenencias.objects.all().order_by('fecha')[:3]
            return queryset
    

class ServiciosView(viewsets.ModelViewSet):
    serializer_class = ServiciosSerializer
    queryset = Servicios.objects.all()
    

class FirstServiciosView(viewsets.ModelViewSet):
    serializer_class = ServiciosSerializer
    
    def get_queryset(self):
        if Servicios.objects.count() == 0:
            return []
        else:
            queryset = Servicios.objects.all().order_by('fecha')[:3]
            return queryset