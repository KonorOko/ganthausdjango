from rest_framework import viewsets
from .serializer import VehiculosSerializer, VerificacionesSerializer, FirstVerificacionesSerializer, TenenciasSerializer, ServiciosSerializer, NotasVehiculosSerializer
from .models import Vehiculos, Verificaciones, Tenencias, Servicios, NotasVehiculos

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
        
        
class NotasVehiculosView(viewsets.ModelViewSet):
    serializer_class = NotasVehiculosSerializer

    def get_queryset(self):
        GROUP_NAME = 'Admin'
        if NotasVehiculos.objects.count() == 0 or not self.request.user.groups.filter(name=GROUP_NAME).exists():
            queryset = NotasVehiculos.objects.none()
            return queryset
        else:
            queryset = NotasVehiculos.objects.all().order_by('id')
            for item in queryset:
                if item.hora == None:
                    item.hora = "--"
                else:
                    item.hora = item.hora.strftime("%H:%M")
                if item.fecha == None:
                    item.fecha = "--"
                else:
                    item.fecha = item.fecha.strftime("%d-%m-%Y")
            return queryset