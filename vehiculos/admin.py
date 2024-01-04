from django.contrib import admin
from .models import Vehiculos, Verificaciones, Tenencias

admin.site.register(Vehiculos)
admin.site.register(Verificaciones)
admin.site.register(Tenencias)