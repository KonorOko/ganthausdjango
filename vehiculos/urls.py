from django.urls import path, include
from rest_framework import routers
from vehiculos import views

router = routers.DefaultRouter()
router.register(r'vehiculos', views.VehiculosView, 'vehiculos')
router.register(r'verificaciones', views.VerificacionesView, 'verificaciones')
router.register(r'first_verificaciones', views.FirstVerificacionesView, 'first_verificaciones')

urlpatterns = [
    path("api/v1/", include(router.urls)),
]