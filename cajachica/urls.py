from django.urls import path, include
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from cajachica import views

router = routers.DefaultRouter()
router.register(r'movimientos', views.MovimientosView, 'movimientos')
router.register(r'balance', views.MovimientosBalance, 'balance')
router.register(r'balance_total', views.BalanceTotal, 'balance_total')
router.register(r'ultimos_movimientos', views.UltimosMovimientos, 'ultimos_movimientos')
router.register(r'movimientos_gasolina', views.MovimientosGasolina, 'movimientos_gasolina')
router.register(r'movimientos_transacciones', views.MovimientosTransacciones, 'movimientos_transacciones')
router.register(r'movimientos_apoyos', views.MovimientosApoyos, 'movimientos_apoyos')
router.register(r'analitics_data', views.AnaliticsData, 'analitics_data')
router.register(r'movimientos_comisiones', views.MovimientosComisiones, 'movimientos_comisiones')

urlpatterns = [
    path("api/v1/", include(router.urls)),
]