from django.urls import path, include
from rest_framework import routers
from vehiculos import views

router = routers.DefaultRouter()
router.register(r'vehiculos', views.VehiculosView, 'vehiculos')
router.register(r'verificaciones', views.VerificacionesView, 'verificaciones')
router.register(r'first_verificaciones', views.FirstVerificacionesView, 'first_verificaciones')
router.register(r'tenencias', views.TenenciasView, 'tenencias')
router.register(r'first_tenencias', views.FirstTenenciasView, 'first_tenencias')
router.register(r'servicios', views.ServiciosView, 'servicios')
router.register(r'first_servicios', views.FirstServiciosView, 'first_servicios')
router.register(r"notas", views.NotasVehiculosView, "notas")
router.register(r"dashboard_notificaciones", views.DashboardNotificacionesView, "dashboard_notificaciones")

urlpatterns = [
    path("api/v1/", include(router.urls)),
]