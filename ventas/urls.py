from django.urls import path, include
from rest_framework import routers
from ventas import views

router = routers.DefaultRouter()
# router.register(r'ventas', views.VentasView, 'ventas')
# router.register(r'ventaspage', views.VentasPageView, 'ventaspage')

urlpatterns = [
    path("api/v1/", include(router.urls)),
]