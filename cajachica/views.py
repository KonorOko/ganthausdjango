from rest_framework import viewsets
from .serializer import MovimientosCajaChicaSerializer, MovimientosBalanceSerializer, BalanceTotalSerializer, MovimientosDataSerializer, AnaliticsDataSerializer, CajaChicaPageSerializer, NotasCajaChicaSerializer, CajaChicaAnalisisSerializer, CajaChicaAnalisisSerializerMid
from .models import MovimientosCajaChica, NotasCajaChica
from django.db.models.functions import Abs
from django.db.models import Sum, Q, Count
from django.utils import timezone
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response
from openpyxl import Workbook
from django.http import HttpResponse
from rest_framework.views import APIView
from django.db.models.functions import TruncMonth
from django.db.models.functions import ExtractDay
from calendar import month_name


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
            queryset = MovimientosCajaChica.objects.order_by(
                'fecha').values('fecha').annotate(cantidad=Sum('cantidad'))
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

        total_cantidad = MovimientosCajaChica.objects.aggregate(
            cantidad_total=Sum('cantidad'))
        total_movimientos = MovimientosCajaChica.objects.aggregate(
            movimientos=Count('id'))

        data = {'cantidad': f"{total_cantidad['cantidad_total']:,.2f}",
                'movimientos': total_movimientos['movimientos']}

        return Response([data])


class UltimosMovimientos(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions,)
    serializer_class = MovimientosCajaChicaSerializer

    def get_queryset(self):
        if MovimientosCajaChica.objects.count() == 0 or self.request.user.groups.filter(name='Admin').exists() == False:
            queryset = MovimientosCajaChica.objects.none()
            return queryset
        else:
            ultimos_movimientos = MovimientosCajaChica.objects.order_by("-id")[:10]
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
        
        
class MovimientosComisiones(viewsets.ModelViewSet):
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
                Q(motivo__icontains='comision') | Q(motivo__icontains='comisiones'))
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
        grouped_comisiones = grouped_data.filter(
            Q(motivo__icontains='comision') | Q(motivo__icontains='comisiones'))
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


class CajaChicaPage(viewsets.GenericViewSet):
    permission_classes = (DjangoModelPermissions,)
    queryset = MovimientosCajaChica.objects.none()
    serializer_class = CajaChicaPageSerializer

    def list(self, request, *args, **kwargs):
        GROUP_NAME = 'Admin'
        today = timezone.now()
        if MovimientosCajaChica.objects.count() == 0 or not self.request.user.groups.filter(name=GROUP_NAME).exists():
            return Response([])

        datos = MovimientosCajaChica.objects.all().order_by('id').all()
        datos_serializer = MovimientosCajaChicaSerializer(datos, many=True)
        balance_total = datos.aggregate(cantidad_total=Sum('cantidad'))[
            'cantidad_total']

        movimientos_grouped = MovimientosCajaChica.objects.filter(
            fecha=today).values('fecha')
        balance_diario = movimientos_grouped.aggregate(
            cantidad=Sum('cantidad'))['cantidad']
        registros_diarios = movimientos_grouped.aggregate(cantidad=Count('id'))[
            'cantidad']

        if today.month == 1:
            balance_mes_anterior = datos.filter(
                fecha__year=today.year - 1, fecha__month=12).aggregate(cantidad=Sum('cantidad'))['cantidad']
        else:
            balance_mes_anterior = datos.filter(
                fecha__year=today.year, fecha__month=today.month - 1).aggregate(cantidad=Sum('cantidad'))['cantidad']

        balance_mensual = datos.filter(
            fecha__year=today.year, fecha__month=today.month).aggregate(cantidad=Sum('cantidad'))['cantidad']

        crecimiento_mensual = 0

        if balance_mensual == None:
            balance_mensual = 0
        if balance_mes_anterior == None:
            balance_mes_anterior = 0
        if balance_diario == None:
            balance_diario = 0

        if registros_diarios == None:
            registros_diarios = 0

        if balance_mes_anterior != 0:
            crecimiento_mensual = (
                balance_mensual - balance_mes_anterior)/balance_mes_anterior * 100

        serializer = CajaChicaPageSerializer(data={
            'datos': datos_serializer.data,
            'balance_total': round(balance_total, 2),
            'balance_diario': round(balance_diario, 2),
            'registros_diarios': registros_diarios,
            'crecimiento_mensual': round(crecimiento_mensual, 2)
        })

        if serializer.is_valid():
            return Response(serializer.data)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=400)


class CajaChicaAnalisis(viewsets.GenericViewSet):
    permission_classes = (DjangoModelPermissions,)
    queryset = MovimientosCajaChica.objects.none()
    serializer_class = CajaChicaAnalisisSerializer

    def list(self, request, *args, **kwargs):
        GROUP_NAME = 'Admin'
        today = timezone.now()
        # or not self.request.user.groups.filter(name=GROUP_NAME).exists():
        if MovimientosCajaChica.objects.count() == 0:
            serializer = CajaChicaAnalisisSerializer(data={
                'balance_anual_agrupado': [{}],
                'balance_total': 0,
                'balance_anual': 0,
                'balance_mensual': 0,
                'balance_diario': 0,
                'registros_anuales': 0,
                'registros_mensuales': 0,
                'registros_diarios': 0,
                'crecimiento_mensual': 0
            })
            return Response(serializer.data)

        # get data
        datos = MovimientosCajaChica.objects.all().order_by('id').all()
        movimientos_grouped = MovimientosCajaChica.objects.filter(
            fecha=today).values('fecha')

        # get total data
        balance_total = datos.aggregate(cantidad_total=Sum('cantidad'))[
            'cantidad_total']

        # get annual data
        balance_anual = datos.filter(fecha__year=today.year).aggregate(
            cantidad=Sum('cantidad'))['cantidad']
        grouped_months = MovimientosCajaChica.objects.filter(Q(fecha__year=today.year) | Q(fecha__year=today.year - 1)).annotate(
            mes=TruncMonth('fecha')).values('mes').annotate(cantidad=Sum('cantidad')).values('mes', 'cantidad')

        # obtiene los datos agrupados por mes para el año actual y el año anterior
        grouped_months_current_year = MovimientosCajaChica.objects.filter(fecha__year=today.year).annotate(
            mes=TruncMonth('fecha')).values('mes').annotate(cantidad=Sum('cantidad')).values('mes', 'cantidad')
        grouped_months_previous_year = MovimientosCajaChica.objects.filter(fecha__year=today.year - 1).annotate(
            mes=TruncMonth('fecha')).values('mes').annotate(cantidad=Sum('cantidad')).values('mes', 'cantidad')

        # convierte los datos agrupados en diccionarios con el mes como clave
        grouped_months_current_year_dict = {
            item['mes'].month: item['cantidad'] for item in grouped_months_current_year}
        grouped_months_previous_year_dict = {
            item['mes'].month: item['cantidad'] for item in grouped_months_previous_year}

        # crea la lista de diccionarios
        balance_anual_agrupado = []
        for i in range(1, 13):
            month_dict = {
                "mes_nombre": month_name[i],
                "año_actual": grouped_months_current_year_dict.get(i, 0),
                "año_anterior": grouped_months_previous_year_dict.get(i, 0),
            }
            if month_dict["año_actual"] == 0:
                del month_dict["año_actual"]
            if month_dict["año_anterior"] == 0:
                del month_dict["año_anterior"]
            balance_anual_agrupado.append(month_dict)

        registros_anuales = datos.filter(fecha__year=today.year).aggregate(
            cantidad=Count('id'))['cantidad']

        # get monthly data
        if today.month == 1:
            balance_mes_anterior = datos.filter(
                fecha__year=today.year - 1, fecha__month=12).aggregate(cantidad=Sum('cantidad'))['cantidad']
        else:
            balance_mes_anterior = datos.filter(
                fecha__year=today.year, fecha__month=today.month - 1).aggregate(cantidad=Sum('cantidad'))['cantidad']

        balance_mensual = datos.filter(
            fecha__year=today.year, fecha__month=today.month).aggregate(cantidad=Sum('cantidad'))['cantidad']

        registros_mensuales = datos.filter(
            fecha__year=today.year, fecha__month=today.month).aggregate(cantidad=Count('id'))['cantidad']

        # get daily data
        balance_diario = movimientos_grouped.aggregate(
            cantidad=Sum('cantidad'))['cantidad']
        registros_diarios = movimientos_grouped.aggregate(cantidad=Count('id'))[
            'cantidad']

        crecimiento_mensual = 0

        if registros_diarios == None:
            registros_diarios = 0
        if balance_anual == None:
            balance_anual = 0
        if balance_mensual == None:
            balance_mensual = 0
        if balance_mes_anterior == None:
            balance_mes_anterior = 0
        if balance_diario == None:
            balance_diario = 0

        if registros_anuales == None:
            registros_anuales = 0
        if registros_mensuales == None:
            registros_mensuales = 0
        if registros_diarios == None:
            registros_diarios = 0

        if balance_mes_anterior != 0:
            crecimiento_mensual = (
                balance_mensual - balance_mes_anterior)/balance_mes_anterior * 100

        serializer = CajaChicaAnalisisSerializer(data={
            'balance_anual_agrupado': balance_anual_agrupado,
            'balance_total': round(balance_total, 2),
            'balance_anual': round(balance_anual, 2),
            'balance_mensual': round(balance_mensual, 2),
            'balance_diario': round(balance_diario, 2),
            'registros_anuales': registros_anuales,
            'registros_mensuales': registros_mensuales,
            'registros_diarios': registros_diarios,
            'crecimiento_mensual': round(crecimiento_mensual, 2)
        })

        if serializer.is_valid():
            return Response(serializer.data)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=400)


class CajaChicaAnalisisMid(viewsets.GenericViewSet):
    # permission_classes = (DjangoModelPermissions,)
    queryset = MovimientosCajaChica.objects.none()
    serializer_class = CajaChicaAnalisisSerializerMid

    def list(self, request, *args, **kwargs):
        GROUP_NAME = 'Admin'
        today = timezone.now()
        # or not self.request.user.groups.filter(name=GROUP_NAME).exists():
        if MovimientosCajaChica.objects.count() == 0:
            pass

        # get data
        grouped_days_current_month = MovimientosCajaChica.objects.filter(fecha__year=today.year, fecha__month=today.month).annotate(
            dia=ExtractDay('fecha')).values('dia').annotate(cantidad=Sum('cantidad')).values('dia', 'cantidad')

        if today.month == 1:
            grouped_days_previous_month = MovimientosCajaChica.objects.filter(fecha__year=today.year - 1, fecha__month=12).annotate(
                dia=ExtractDay('fecha')).values('dia').annotate(cantidad=Sum('cantidad')).values('dia', 'cantidad')
        else:
            grouped_days_previous_month = MovimientosCajaChica.objects.filter(fecha__year=today.year, fecha__month=today.month - 1).annotate(
                dia=ExtractDay('fecha')).values('dia').annotate(cantidad=Sum('cantidad')).values('dia', 'cantidad')
            
        grouped_weeks_current_month_dict = {}
        grouped_weeks_previous_month_dict = {}

        for item in grouped_days_current_month:
            dia = item['dia']
            cantidad = item['cantidad']

            semana = (dia - 1) // 7 + 1

            grouped_weeks_current_month_dict[semana] = grouped_weeks_current_month_dict.get(semana, 0) + cantidad
        
        for item in grouped_days_previous_month:
            dia = item['dia']
            cantidad = item['cantidad']

            semana = (dia - 1) // 7 + 1

            grouped_weeks_previous_month_dict[semana] = grouped_weeks_previous_month_dict.get(semana, 0) + cantidad

        comparation_month = []
        for i in range(1, 5):
            week_dict = {
                "semana": i,
                "Mes Actual": grouped_weeks_current_month_dict.get(i, 0),
                "Mes Anterior": grouped_weeks_previous_month_dict.get(i, 0),
            }
            comparation_month.append(week_dict)

        grouped_data = (MovimientosCajaChica
                        .objects.values('motivo')
                        .annotate(grouped_cantidad=Sum('cantidad'))
                        .filter(cantidad__lt=0, fecha__month=today.month, fecha__year=today.year))

        # gasolina
        grouped_gasolina = grouped_data.filter(
            motivo__contains='GASOLINA').aggregate(cantidad_total=Sum(Abs('grouped_cantidad')))['cantidad_total']

        # transferencias
        grouped_transacciones = grouped_data.filter(
            Q(motivo__contains='TRANSFERENCIA') | Q(motivo__contains='DEPOSITO')).aggregate(cantidad_total=Sum(Abs('grouped_cantidad')))['cantidad_total']

        # comisiones
        grouped_comisiones = grouped_data.filter(
            Q(motivo__contains='COMISION') | Q(motivo__contains='COMISIONES')).aggregate(cantidad_total=Sum(Abs('grouped_cantidad')))['cantidad_total']

        # oficina
        grouped_oficina = grouped_data.filter(
            motivo__contains='OFICINA').aggregate(cantidad_total=Sum(Abs('grouped_cantidad')))['cantidad_total']

        # otros
        grouped_otros = grouped_data.filter(
            ~Q(motivo__contains='GASOLINA') & ~Q(motivo__contains='TRASNFERENCIA') & ~Q(motivo__contains='COMISION') & ~Q(motivo__contains='COMISIONES') & ~Q(motivo__contains='OFICINA')).aggregate(cantidad_total=Sum(Abs('grouped_cantidad')))['cantidad_total']

        if grouped_gasolina == None:
            grouped_gasolina = 0
        if grouped_transacciones == None:
            grouped_transacciones = 0
        if grouped_comisiones == None:
            grouped_comisiones = 0
        if grouped_oficina == None:
            grouped_oficina = 0
        if grouped_otros == None:
            grouped_otros = 0

        serializer = CajaChicaAnalisisSerializerMid(data={
            'comparativa_mensual': comparation_month,
            'tipos_de_egresos': [
                {'motivo':'gasolina', 'cantidad': grouped_gasolina},
                {'motivo':'transacciones', 'cantidad': grouped_transacciones},
                {'motivo':'comisiones', 'cantidad': grouped_comisiones},
                {'motivo':'oficina', 'cantidad': grouped_oficina},
                {'motivo':'otros', 'cantidad': grouped_otros,}
            ]
        })

        if serializer.is_valid():
            return Response(serializer.data)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=400)


class CajaChicaExcel(APIView):
    permission_classes = (DjangoModelPermissions,)
    queryset = MovimientosCajaChica.objects.none()

    def get(self, request, *args, **kwargs):
        datos = MovimientosCajaChica.objects.all().order_by('-id').all()
        wb = Workbook()
        ws = wb.active
        ws.column_dimensions['B'].width = 11
        ws.column_dimensions['C'].width = 35
        ws.column_dimensions['D'].width = 11
        ws.append(['ID', 'FECHA', 'MOTIVO', 'CANTIDAD'])
        for dato in datos:
            ws.append([dato.id, dato.fecha, dato.motivo, dato.cantidad])
        nombre_archivo = f"caja_chica_{timezone.now().strftime('%d-%m-%Y')}.xlsx"
        response = HttpResponse(content_type="application/ms-excel")
        contenido = "attachment; filename = {0}".format(nombre_archivo)
        response["Content-Disposition"] = contenido
        wb.save(response)
        return response


class NotasCajaChicaView(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions,)
    serializer_class = NotasCajaChicaSerializer

    def get_queryset(self):
        if NotasCajaChica.objects.count() == 0 or self.request.user.groups.filter(name='Admin').exists() == False:
            queryset = NotasCajaChica.objects.none()
            return queryset
        else:
            queryset = NotasCajaChica.objects.all().order_by('id')
            for item in queryset:
                item.hora = item.hora.strftime("%H:%M")
            return queryset
