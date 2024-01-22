from rest_framework import viewsets
from .serializer import MovimientosCajaChicaSerializer, CajaChicaPageSerializer, NotasCajaChicaSerializer, CajaChicaAnalisisSerializer, CajaChicaAnalisisSerializerMid, CajaChicaAnalisisVehiculosSerializer, DashboardCajaChicaSerializer, DashboardNotificacionesSerializer
from .models import MovimientosCajaChica, NotasCajaChica
from django.db.models.functions import Abs
from django.db.models import Sum, Q, Count
from django.db.models.functions import TruncDay
from django.utils import timezone
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response
from openpyxl import Workbook
from django.http import HttpResponse
from rest_framework.views import APIView
from django.db.models.functions import TruncMonth
from django.db.models.functions import ExtractDay
from dateutil.relativedelta import relativedelta
from collections import defaultdict

MONTH_NAMES = ["", "Ene", "Feb", "Mar", "Abr", "May",
               "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]


class MovimientosView(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions,)
    serializer_class = MovimientosCajaChicaSerializer

    def get_queryset(self):
        if MovimientosCajaChica.objects.count() == 0 or self.request.user.groups.filter(name='Admin').exists() == False:
            queryset = MovimientosCajaChica.objects.none()
        else:
            queryset = MovimientosCajaChica.objects.all().order_by('id')
        return queryset


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
        print(serializer)
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
        if MovimientosCajaChica.objects.count() == 0 or not self.request.user.groups.filter(name=GROUP_NAME).exists():
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
            if serializer.is_valid():
                return Response(serializer.data)
            else:
                print(serializer.errors)
                return Response(serializer.errors, status=400)

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

        grouped_months_current_year = MovimientosCajaChica.objects.filter(fecha__year=today.year).annotate(
            mes=TruncMonth('fecha')).values('mes').annotate(cantidad=Sum('cantidad')).values('mes', 'cantidad')
        grouped_months_previous_year = MovimientosCajaChica.objects.filter(fecha__year=today.year - 1).annotate(
            mes=TruncMonth('fecha')).values('mes').annotate(cantidad=Sum('cantidad')).values('mes', 'cantidad')

        grouped_months_current_year_dict = {
            item['mes'].month: item['cantidad'] for item in grouped_months_current_year}
        grouped_months_previous_year_dict = {
            item['mes'].month: item['cantidad'] for item in grouped_months_previous_year}

        balance_anual_agrupado = []
        for i in range(1, 13):
            month_dict = {
                "mes_nombre": MONTH_NAMES[i],
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
    permission_classes = (DjangoModelPermissions,)
    queryset = MovimientosCajaChica.objects.none()
    serializer_class = CajaChicaAnalisisSerializerMid

    def list(self, request, *args, **kwargs):
        GROUP_NAME = 'Admin'
        today = timezone.now()

        if MovimientosCajaChica.objects.count() == 0 or not self.request.user.groups.filter(name=GROUP_NAME).exists():
            serializer = CajaChicaAnalisisSerializerMid(data={
                'comparativa_mensual': [{
                    'semana': 1,
                    'Mes Actual': 0,
                    'Mes Anterior': 0
                }, {
                    'semana': 2,
                    'Mes Actual': 0,
                    'Mes Anterior': 0
                }, {
                    'semana': 3,
                    'Mes Actual': 0,
                    'Mes Anterior': 0
                }, {
                    'semana': 4,
                    'Mes Actual': 0,
                    'Mes Anterior': 0}],
                'tipos_de_egresos': [
                    {'motivo': 'gasolina', 'cantidad': 0},
                    {'motivo': 'transacciones', 'cantidad': 0},
                    {'motivo': 'comisiones', 'cantidad': 0},
                    {'motivo': 'oficina', 'cantidad': 0},
                    {'motivo': 'otros', 'cantidad': 0}
                ]
            })
            if serializer.is_valid():
                return Response(serializer.data)
            else:
                print(serializer.errors)
                return Response(serializer.errors, status=400)

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

            grouped_weeks_current_month_dict[semana] = grouped_weeks_current_month_dict.get(
                semana, 0) + cantidad

        for item in grouped_days_previous_month:
            dia = item['dia']
            cantidad = item['cantidad']

            semana = (dia - 1) // 7 + 1

            grouped_weeks_previous_month_dict[semana] = grouped_weeks_previous_month_dict.get(
                semana, 0) + cantidad

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
            motivo__contains='GASOLINA', cantidad__lt=0, motivo__regex=r'^\d{2}').aggregate(cantidad_total=Sum(Abs('grouped_cantidad')))['cantidad_total']

        # transferencias
        grouped_transacciones = grouped_data.filter(
            Q(motivo__contains='TRANSFERENCIA') | Q(motivo__contains='DEPOSITO'), cantidad__lt=0).aggregate(cantidad_total=Sum(Abs('grouped_cantidad')))['cantidad_total']

        # comisiones
        grouped_comisiones = grouped_data.filter(
            Q(motivo__contains='COMISION') | Q(motivo__contains='COMISIONES'), cantidad__lt=0).aggregate(cantidad_total=Sum(Abs('grouped_cantidad')))['cantidad_total']

        # oficina
        grouped_oficina = grouped_data.filter(
            motivo__contains='OFICINA', cantidad__lt=0).aggregate(cantidad_total=Sum(Abs('grouped_cantidad')))['cantidad_total']

        # apoyos
        grouped_apoyos = grouped_data.filter(
            motivo__contains='APOYO', cantidad__lt=0).aggregate(cantidad_total=Sum(Abs('grouped_cantidad')))['cantidad_total']

        # pagos
        grouped_pagos = grouped_data.filter(
            Q(motivo__contains='PAGO') | Q(motivo__contains='PAGOS'), cantidad__lt=0).aggregate(cantidad_total=Sum(Abs('grouped_cantidad')))['cantidad_total']

        # sueldos
        grouped_sueldos = grouped_data.filter(
            motivo__contains='SUELDO', cantidad__lt=0).aggregate(cantidad_total=Sum(Abs('grouped_cantidad')))['cantidad_total']

        # otros
        grouped_otros = grouped_data.filter(
            ~Q(motivo__contains='GASOLINA') & ~Q(motivo__contains='TRASNFERENCIA') & ~Q(motivo__contains='DEPOSITO') & ~Q(motivo__contains='COMISION') & ~Q(motivo__contains='COMISIONES') & ~Q(motivo__contains='OFICINA') & ~Q(motivo__contains='APOYO') & ~Q(motivo__contains='PAGO') & ~Q(motivo__contains='PAGOS') & ~Q(motivo__contains='SUELDO'), cantidad__lt=0).aggregate(cantidad_total=Sum(Abs('grouped_cantidad')))['cantidad_total']

        if grouped_gasolina == None:
            grouped_gasolina = 0
        if grouped_transacciones == None:
            grouped_transacciones = 0
        if grouped_comisiones == None:
            grouped_comisiones = 0
        if grouped_oficina == None:
            grouped_oficina = 0
        if grouped_apoyos == None:
            grouped_apoyos = 0
        if grouped_pagos == None:
            grouped_pagos = 0
        if grouped_sueldos == None:
            grouped_sueldos = 0
        if grouped_otros == None:
            grouped_otros = 0

        serializer = CajaChicaAnalisisSerializerMid(data={
            'comparativa_mensual': comparation_month,
            'tipos_de_egresos': [
                {'motivo': 'gasolina', 'cantidad': grouped_gasolina},
                {'motivo': 'transacciones', 'cantidad': grouped_transacciones},
                {'motivo': 'comisiones', 'cantidad': grouped_comisiones},
                {'motivo': 'oficina', 'cantidad': grouped_oficina},
                {'motivo': 'apoyos', 'cantidad': grouped_apoyos},
                {'motivo': 'pagos', 'cantidad': grouped_pagos},
                {'motivo': 'sueldos', 'cantidad': grouped_sueldos},
                {'motivo': 'otros', 'cantidad': grouped_otros, }
            ]
        })

        if serializer.is_valid():
            return Response(serializer.data)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=400)


class CajaChicaAnalisisVehiculos(viewsets.GenericViewSet):
    permission_classes = (DjangoModelPermissions,)
    queryset = MovimientosCajaChica.objects.none()
    serializer_class = CajaChicaAnalisisVehiculosSerializer

    def list(self, request, *args, **kwargs):
        GROUP_NAME = 'Admin'
        today = timezone.now()
        if MovimientosCajaChica.objects.count() == 0 or not self.request.user.groups.filter(name=GROUP_NAME).exists():
            pass

        # get data
        balance_mensual = MovimientosCajaChica.objects.filter(
            fecha__year=today.year, fecha__month=today.month, motivo__contains='GASOLINA', motivo__regex=r'^\d{2}', cantidad__lt=0).aggregate(cantidad=Abs(Sum('cantidad')))['cantidad']

        four_months_ago = (today - relativedelta(months=3)).replace(day=1)

        data_last_4_months = MovimientosCajaChica.objects.filter(
            fecha__gte=four_months_ago, motivo__contains='GASOLINA'
        ).annotate(
            mes=TruncMonth('fecha')
        ).values(
            'mes'
        ).annotate(
            cantidad=Abs(Sum('cantidad'))
        ).values('mes', 'cantidad', 'motivo')

        data_last_4_months_format = []
        vehiculos = ['01', '02', '03', '04', '05', '06']
        data_by_month = defaultdict(dict)

        # Iterar sobre los datos
        for data in data_last_4_months:
            # Obtener el mes y el motivo
            mes = data['mes'].month
            motivo = data['motivo'][:2]

            # Si el motivo está en la lista de vehículos, agregarlo al diccionario
            if motivo in vehiculos:
                # Si el mes ya está en el diccionario, sumar la cantidad
                if mes in data_by_month and motivo in data_by_month[mes]:
                    data_by_month[mes][motivo] += data['cantidad']
                else:
                    # Si el mes o el motivo no están en el diccionario, inicializar la cantidad
                    data_by_month[mes][motivo] = data['cantidad']

        # Convertir el diccionario a una lista de diccionarios
        data_last_4_months_format = [{'mes': mes, **motivos}
                                     for mes, motivos in data_by_month.items()]

        top_4_vehiculos = MovimientosCajaChica.objects.filter(
            fecha__gte=four_months_ago, motivo__contains='GASOLINA', motivo__regex=r'^\d{2}', cantidad__lt=0
        ).values(
            'motivo'
        ).annotate(
            cantidad=Abs(Sum('cantidad'))
        ).order_by(
            '-cantidad'
        )[:4]

        top_4_vehiculos = list(top_4_vehiculos)
        top_4_vehiculos_format = []
        for item in range(1, 5):
            if item <= len(top_4_vehiculos):
                top = {
                    'top': item,
                    'vehiculo': top_4_vehiculos[item-1]['motivo'][:2],
                    'cantidad': top_4_vehiculos[item-1]['cantidad']
                }
            else:
                top = {
                    'top': item,
                    'vehiculo': '00',
                    'cantidad': 0
                }
            top_4_vehiculos_format.append(top)

        data_year = MovimientosCajaChica.objects.filter(
            fecha__year=today.year, motivo__contains='GASOLINA', motivo__regex=r'^\d{2}', cantidad__lt=0
        ).annotate(
            mes=TruncMonth('fecha')
        ).values(
            'mes'
        ).annotate(
            cantidad=Abs(Sum('cantidad'))
        ).values('mes', 'cantidad', 'motivo')

        data_year_grouped = defaultdict(int)

        for item in data_year:
            # Sumar la cantidad al total para este mes
            data_year_grouped[item['mes'].month] += item['cantidad']

        data_year_grouped_format = []
        for i in range(1, 13):
            month_dict = {
                "mes": MONTH_NAMES[i],
                "cantidad": data_year_grouped.get(i, 0),
            }
            data_year_grouped_format.append(month_dict)

        if balance_mensual == None:
            balance_mensual = 0

        serializer = CajaChicaAnalisisVehiculosSerializer(data={
            'consumo_gasolina_mensual': balance_mensual,
            'vehiculos_mayor_consumo_4_meses': top_4_vehiculos_format,
            'datos_ultimos_4_meses': data_last_4_months_format,
            'consumo_anual': data_year_grouped_format,
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
        GROUP_NAME = 'Admin'
        if NotasCajaChica.objects.count() == 0 or not self.request.user.groups.filter(name=GROUP_NAME).exists():
            queryset = NotasCajaChica.objects.none()
            return queryset
        else:
            queryset = NotasCajaChica.objects.all().order_by('id')
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


class DashboardCajaChica(viewsets.GenericViewSet):
    permission_classes = (DjangoModelPermissions,)
    queryset = MovimientosCajaChica.objects.none()
    serializer_class = DashboardCajaChicaSerializer

    def list(self, request, *args, **kwargs):
        GROUP_NAME = 'Admin'
        today = timezone.now()
        if MovimientosCajaChica.objects.count() == 0 or not self.request.user.groups.filter(name=GROUP_NAME).exists():
            pass
        # get data
        balance_total = MovimientosCajaChica.objects.all().aggregate(cantidad_total=Sum('cantidad'))[
            'cantidad_total']

        # get monthly data total balance per day
        data_per_day = MovimientosCajaChica.objects.annotate(day=TruncDay('fecha')).values('day').annotate(cantidad_total=Sum('cantidad')).order_by('day')

        # calculate cumulative sum
        cumulative_sum = 0
        cumulative_data = []
        for data in data_per_day:
            cumulative_sum += data['cantidad_total']
            cumulative_data.append({'día': data['day'].day, 'cantidad': cumulative_sum})

        # revenue
        revenue = MovimientosCajaChica.objects.filter(
            fecha__year=today.year, fecha__month=today.month, cantidad__gt=0).aggregate(cantidad=Sum('cantidad'))['cantidad']
        
        # expenses
        expenses = MovimientosCajaChica.objects.filter(
            fecha__year=today.year, fecha__month=today.month, cantidad__lt=0).aggregate(cantidad=Sum(Abs('cantidad')))['cantidad']

        if revenue == None:
            revenue = 0
        if expenses == None:
            expenses = 0
        if balance_total == None:
            balance_total = 0
        if cumulative_data == None:
            cumulative_data = []

        serializer = DashboardCajaChicaSerializer(data={
            'balance_total': round(balance_total, 2),
            'ingresos': round(revenue, 2),
            'egresos': round(expenses, 2),
            'registros': cumulative_data
        })

        if serializer.is_valid():
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

class DashboardNotificaciones(viewsets.GenericViewSet):
    pass