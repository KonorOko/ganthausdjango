# from .serializer import VentasSerializer, VentasPageSerializerID, VentasPageSerializer
# from rest_framework import viewsets
# from .models import Ventas
# from rest_framework.response import Response
# from django.db.models import Sum

# # Create your views here.
# class VentasView(viewsets.ModelViewSet):
#     queryset = Ventas.objects.all()
#     serializer_class = VentasSerializer


# class VentasPageView(viewsets.GenericViewSet):
#     serializer_class = VentasPageSerializer
#     queryset = Ventas.objects.all()
#     serializer_class = VentasPageSerializer

#     def list(self, request, *args, **kwargs):
#         data = Ventas.objects.all().order_by('id').all()
#         data_serializer = VentasSerializer(data, many=True)
        
#         monthly_sales = Ventas.objects.all().aggregate(Sum('pagado'))["pagado__sum"]
        
#         serializer = VentasPageSerializer(data={"data": data_serializer.data, "monthly_sales": monthly_sales})
        
#         if serializer.is_valid():
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
        
        
