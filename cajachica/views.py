from rest_framework import viewsets
from .serializer import MovimientosCajaChicaSerializer, MovimientosBalanceSerializer, BalanceTotalSerializer, MovimientosDataSerializer, AnaliticsDataSerializer
from .models import MovimientosCajaChica
from django.db.models.functions import Abs
from django.db.models import Sum, Q, Count
from django.utils import timezone
from rest_framework.permissions import  DjangoModelPermissions
from rest_framework.response import Response

class MovimientosView(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions,)
    serializer_class = MovimientosCajaChicaSerializer

    def get_queryset(self):
        if MovimientosCajaChica.objects.count() == 0 or self.request.user.groups.filter(name='Admin').exists() == False:
            queryset = MovimientosCajaChica.objects.none()
        else:
            queryset = MovimientosCajaChica.objects.all().order_by('id')
        return queryset


class MovimientosBalance(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions,)
    serializer_class = MovimientosBalanceSerializer

    def get_queryset(self):
        if MovimientosCajaChica.objects.count() == 0 or not self.request.user.groups.filter(name='Admin').exists():
            return MovimientosCajaChica.objects.none()
        else:
            queryset = MovimientosCajaChica.objects.order_by('fecha').values('fecha').annotate(cantidad=Sum('cantidad'))
            balance_acumulativo = 0
            for item in queryset:
                balance_acumulativo += item['cantidad']
                item['cantidad'] = balance_acumulativo

            return queryset
        
        
class BalanceTotal(viewsets.ModelViewSet):
    serializer_class = BalanceTotalSerializer
    permission_classes = (DjangoModelPermissions,)

    def get_queryset(self):
        return MovimientosCajaChica.objects.none()

    def list(self, request, *args, **kwargs):
        if MovimientosCajaChica.objects.count() == 0:
            return Response([])

        total_cantidad = MovimientosCajaChica.objects.aggregate(cantidad_total=Sum('cantidad'))
        total_movimientos = MovimientosCajaChica.objects.aggregate(movimientos=Count('id'))

        data = {'cantidad': f"{total_cantidad['cantidad_total']:,.2f}", 'movimientos': total_movimientos['movimientos']}

        return Response([data])
    

class UltimosMovimientos(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions,)
    serializer_class = MovimientosCajaChicaSerializer

    def get_queryset(self):
        if MovimientosCajaChica.objects.count() == 0 or self.request.user.groups.filter(name='Admin').exists() == False:
            queryset = MovimientosCajaChica.objects.none()
            return queryset
        else:
            ultimos_movimientos = MovimientosCajaChica.objects.all()[:10]
            return ultimos_movimientos


class MovimientosGasolina(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions,)
    serializer_class = MovimientosDataSerializer

    def get_queryset(self):
        if MovimientosCajaChica.objects.count() == 0 or self.request.user.groups.filter(name='Admin').exists() == False:
            queryset = MovimientosCajaChica.objects.none()
            return queryset
        else:
            today = timezone.now()
            grouped_data = (MovimientosCajaChica
                            .objects.values('motivo')
                            .annotate(cantidad=Sum(Abs('cantidad')))
                            .filter(fecha__month=today.month))
            grouped_transferencias = grouped_data.filter(
                motivo__icontains='gasolina')
            queryset = grouped_transferencias
            return queryset


class MovimientosTransacciones(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions,)
    serializer_class = MovimientosDataSerializer

    def get_queryset(self):
        if MovimientosCajaChica.objects.count() == 0 or self.request.user.groups.filter(name='Admin').exists() == False:
            queryset = MovimientosCajaChica.objects.none()
            return queryset
        else:
            today = timezone.now()
            grouped_data = (MovimientosCajaChica
                            .objects.values('motivo')
                            .annotate(cantidad=Sum(Abs('cantidad')))
                            .filter(fecha__month=today.month))
            grouped_transferencias = grouped_data.filter(
                Q(motivo__icontains='transferencia') | Q(motivo__icontains='deposito'))
            queryset = grouped_transferencias
            return queryset


class MovimientosApoyos(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions,)
    serializer_class = MovimientosDataSerializer

    def get_queryset(self):
        if MovimientosCajaChica.objects.count() == 0 or self.request.user.groups.filter(name='Admin').exists() == False:
            queryset = MovimientosCajaChica.objects.none()
            return queryset
        else:
            today = timezone.now()
            grouped_data = (MovimientosCajaChica
                            .objects.values('motivo')
                            .annotate(cantidad=Sum(Abs('cantidad')))
                            .filter(fecha__month=today.month))
            grouped_transferencias = grouped_data.filter(
                motivo__icontains='apoyo')
            queryset = grouped_transferencias
            return queryset


class AnaliticsData(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions,)
    serializer_class = AnaliticsDataSerializer

    def get_queryset(self):
        if MovimientosCajaChica.objects.count() == 0 or not self.request.user.groups.filter(name='Admin').exists():
            return MovimientosCajaChica.objects.none()
        return MovimientosCajaChica.objects.all()
    def list(self, request, *args, **kwargs):
        if MovimientosCajaChica.objects.count() == 0 or not self.request.user.groups.filter(name='Admin').exists():
            return Response([])

        today = timezone.now()
        today.month
        grouped_data = (MovimientosCajaChica
                        .objects.values('motivo')
                        .annotate(grouped_cantidad=Sum('cantidad'))
                        .filter(fecha__month=today.month))

        # gasolina
        grouped_gasolina = grouped_data.filter(
            motivo__icontains='gasolina')
        gasolina_total = grouped_gasolina.aggregate(
            cantidad_total_abs=Sum(Abs('grouped_cantidad')))
        if gasolina_total['cantidad_total_abs'] == None:
            gasolina_total['cantidad_total_abs'] = 0
        dict_gasolina = {"motivo": "gasolina",
                            'cantidad_total': f'{gasolina_total["cantidad_total_abs"]:,.2f}'}

        # transferencias
        grouped_transferencias = grouped_data.filter(
            Q(motivo__icontains='transferencia') | Q(motivo__icontains='deposito'))
        transferencias_total = grouped_transferencias.aggregate(
            cantidad_total_abs=Sum(Abs('grouped_cantidad')))
        if transferencias_total['cantidad_total_abs'] == None:
            transferencias_total['cantidad_total_abs'] = 0
        dict_transferencias = {"motivo": "transferencias",
                                'cantidad_total': f'{transferencias_total["cantidad_total_abs"]:,.2f}'}

        # apoyos
        grouped_apoyos = grouped_data.filter(motivo__icontains='apoyo')
        apoyos_total = grouped_apoyos.aggregate(
            cantidad_total_abs=Sum(Abs('grouped_cantidad')))
        if apoyos_total['cantidad_total_abs'] == None:
            apoyos_total['cantidad_total_abs'] = 0
        dict_apoyos = {"motivo": "apoyos",
                        'cantidad_total': f'{apoyos_total["cantidad_total_abs"]:,.2f}'}
        
        # comisiones
        grouped_comisiones = grouped_data.filter(Q(motivo__icontains='comision') | Q(motivo__icontains='comisiones'))
        comisiones_total = grouped_comisiones.aggregate(
            cantidad_total_abs=Sum(Abs('grouped_cantidad')))
        if comisiones_total['cantidad_total_abs'] == None:
            comisiones_total['cantidad_total_abs'] = 0
        dict_comisiones = {"motivo": "comisiones",
                        'cantidad_total': f'{comisiones_total["cantidad_total_abs"]:,.2f}'}

        # otros
        otros_registros = (
            MovimientosCajaChica.objects
            .exclude(motivo__icontains='gasolina')
            .exclude(motivo__icontains='transferencia')
            .exclude(motivo__icontains='apoyo')
            .filter(cantidad__lt=0, fecha__month=today.month)
            .values('motivo')
            .annotate(total=Sum('cantidad'))
        )
        otros_total = otros_registros.aggregate(
            cantidad_total_abs=Sum(Abs('total')))
        if otros_total['cantidad_total_abs'] == None:
            otros_total['cantidad_total_abs'] = 0
        dict_otros = {"motivo": "otros",
                        'cantidad_total': f'{otros_total["cantidad_total_abs"]:,.2f}'}

        queryset = [dict_gasolina, dict_transferencias,
                    dict_apoyos, dict_comisiones, dict_otros]
        
        return Response(queryset)
