from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from rest_framework.documentation import include_docs_urls
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cajachica/', include('cajachica.urls')),
    path('vehiculos/', include('vehiculos.urls')),
    path('', include('authentification.urls')),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name ='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name ='token_refresh'),
    path("docs/", include_docs_urls(title="Documentación API")),
]
