from datetime import datetime
from rest_framework import viewsets
from .serializer import MovimientosCajaChicaSerializer, MovimientosBalanceSerializer, BalanceTotalSerializer, MovimientosDataSerializer, AnaliticsDataSerializer
from .models import MovimientosCajaChica
from django.db.models.functions import Abs
from django.db.models import Sum, Q
from django.utils import timezone
import pandas as pd


class MovimientosView(viewsets.ModelViewSet):
    serializer_class = MovimientosCajaChicaSerializer
    queryset = MovimientosCajaChica.objects.all()


class MovimientosBalance(viewsets.ModelViewSet):
    serializer_class = MovimientosBalanceSerializer

    def get_queryset(self):
        if MovimientosCajaChica.objects.count() == 0:
            return []
        else:
            df = pd.DataFrame(MovimientosCajaChica.objects.all().values())
            monto_total = df.groupby("fecha")["cantidad"].sum().reset_index()
            monto_total["cantidad"] = monto_total["cantidad"].cumsum()
            queryset = monto_total.to_dict("records")
            return queryset


class BalanceTotal(viewsets.ModelViewSet):
    serializer_class = BalanceTotalSerializer

    def get_queryset(self):
        if MovimientosCajaChica.objects.count() == 0:
            return []
        else:
            df = pd.DataFrame(MovimientosCajaChica.objects.all().values())
            balance_total = df['cantidad'].sum()
            movimientos = df['cantidad'].count()
            queryset = [{'cantidad': f"{balance_total: ,.2f}",
                         'movimientos': movimientos}]
            return queryset


class UltimosMovimientos(viewsets.ModelViewSet):
    serializer_class = MovimientosCajaChicaSerializer

    def get_queryset(self):
        if MovimientosCajaChica.objects.count() == 0:
            return []
        else:
            df = pd.DataFrame(MovimientosCajaChica.objects.all().values())
            ultimos_movimientos = df.tail(10).to_dict("records")
            return ultimos_movimientos


class MovimientosGasolina(viewsets.ModelViewSet):
    serializer_class = MovimientosDataSerializer

    def get_queryset(self):
        if MovimientosCajaChica.objects.count() == 0:
            return []
        else:
            today = timezone.now()
            grouped_data = (MovimientosCajaChica
                            .objects.values('motivo')
                            .annotate(cantidad=Sum(Abs('cantidad')))
                            .filter(fecha__month=today.month))
            grouped_transferencias = grouped_data.filter(motivo__icontains='gasolina')
            queryset = grouped_transferencias
            return queryset

class MovimientosTransacciones(viewsets.ModelViewSet):
    serializer_class = MovimientosDataSerializer
    
    def get_queryset(self):
        if MovimientosCajaChica.objects.count() == 0:
            return []
        else:
            today = timezone.now()
            grouped_data = (MovimientosCajaChica
                            .objects.values('motivo')
                            .annotate(cantidad=Sum(Abs('cantidad')))
                            .filter(fecha__month=today.month))
            grouped_transferencias = grouped_data.filter(Q(motivo__icontains='transferencia') | Q(motivo__icontains='deposito'))
            queryset = grouped_transferencias
            return queryset
        
class MovimientosApoyos(viewsets.ModelViewSet):
    serializer_class = MovimientosDataSerializer
    
    def get_queryset(self):
        if MovimientosCajaChica.objects.count() == 0:
            return []
        else:
            today = timezone.now()
            grouped_data = (MovimientosCajaChica
                            .objects.values('motivo')
                            .annotate(cantidad=Sum(Abs('cantidad')))
                            .filter(fecha__month=today.month))
            grouped_transferencias = grouped_data.filter(motivo__icontains='apoyo')
            queryset = grouped_transferencias
            return queryset

class AnaliticsData(viewsets.ModelViewSet):
    serializer_class = AnaliticsDataSerializer

    def get_queryset(self):
        if MovimientosCajaChica.objects.count() == 0:
            return []
        else:
            today = timezone.now()
            today.month
            grouped_data = (MovimientosCajaChica
                            .objects.values('motivo')
                            .annotate(grouped_cantidad=Sum('cantidad'))
                            .filter(fecha__month=today.month))
            
            # gasolina
            grouped_gasolina = grouped_data.filter(motivo__icontains='gasolina')
            gasolina_total = grouped_gasolina.aggregate(cantidad_total_abs=Sum(Abs('grouped_cantidad')))
            dict_gasolina = {"motivo": "gasolina", 'cantidad_total': gasolina_total['cantidad_total_abs']}
            
            # transferencias
            grouped_transferencias = grouped_data.filter(Q(motivo__icontains='transferencia') | Q(motivo__icontains='deposito'))
            transferencias_total = grouped_transferencias.aggregate(cantidad_total_abs=Sum(Abs('grouped_cantidad')))
            dict_transferencias = {"motivo": "transferencias", 'cantidad_total': transferencias_total['cantidad_total_abs']}
            
            # apoyos
            grouped_apoyos = grouped_data.filter(motivo__icontains='apoyo')
            apoyos_total = grouped_apoyos.aggregate(cantidad_total_abs=Sum(Abs('grouped_cantidad')))
            dict_apoyos = {"motivo": "apoyos", 'cantidad_total': apoyos_total['cantidad_total_abs']} 
            
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
            otros_total = otros_registros.aggregate(cantidad_total_abs=Sum(Abs('total')))
            dict_otros = {"motivo": "otros", 'cantidad_total': otros_total['cantidad_total_abs']}
            
            queryset = [dict_gasolina, dict_transferencias, dict_apoyos, dict_otros]
            return queryset
