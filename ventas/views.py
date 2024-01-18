from .serializer import VentaSerializer
from rest_framework import viewsets
from .models import Ventas

# Create your views here.
class VentasView(viewsets.ModelViewSet):
    queryset = Ventas.objects.all()
    serializer_class = VentaSerializer