from django.contrib import admin
from .models import Device, TemperatureReading, HumidityReading

# Register your models here.

admin.site.register(Device)
admin.site.register(TemperatureReading)
admin.site.register(HumidityReading)
