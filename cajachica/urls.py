from django.urls import path, include
from rest_framework import routers
from cajachica import views

router = routers.DefaultRouter()
router.register(r'movimientos', views.MovimientosView, 'movimientos')
router.register(r'cajachica_page', views.CajaChicaPage, 'cajachica_page')
router.register(r'notas', views.NotasCajaChicaView, 'notas')
router.register(r'cajachica_analisis', views.CajaChicaAnalisis, 'cajachica_analisis')
router.register(r'cajachica_analisismid', views.CajaChicaAnalisisMid, 'cajachica_analisismid')
router.register(r'cajachica_analisisvehiculos', views.CajaChicaAnalisisVehiculos, 'cajachica_analisisvehiculos')

urlpatterns = [
    path("api/v1/", include(router.urls)),
    path("api/v1/cajachica_excel/", views.CajaChicaExcel.as_view(), name="cajachica_excel"),
]